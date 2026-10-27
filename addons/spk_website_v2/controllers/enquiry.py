# -*- coding: utf-8 -*-
"""The public enquiry endpoint: ``POST /website/spk/enquiry``.

An ordinary form POST with Odoo's CSRF token, enhanced by
static/src/js/enquiry.js (which sends the same form and asks for JSON). Only
allowlisted fields are read; everything server-owned (website, company, team,
salesperson) is chosen here. Success is reported only once the lead exists.
"""

import logging
import re

from odoo import http
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.tools import email_normalize

from .. import site_content as content
from ..models.crm_lead import CONFLICT, CREATED, DUPLICATE
from ..rendering import is_preview, is_v2_enabled
from .main import _lang, render_contact

_logger = logging.getLogger(__name__)

HONEYPOT_FIELD = "spk_website_check"
CAPTCHA_ACTION = "website_form"  # the action Odoo's website forms use for their captcha
MAX_BODY_BYTES = 32 * 1024
SUBMISSION_ID_RE = re.compile(r"^[0-9a-f]{32}$")
UTM_RE = re.compile(r"^[A-Za-z0-9 ._+\-]*$")
PHONE_RE = re.compile(r"^[0-9+().\-\s/xX]*$")

MESSAGES = {
    "name": "Enter your name, between 2 and 120 characters.",
    "email": "Enter a valid email address.",
    "enquiry_type": "Choose what you would like help with.",
    "company": "Use 160 characters or fewer for the company.",
    "region": "Use 100 characters or fewer for the country or region.",
    "details": "Use 4,000 characters or fewer for the project details.",
    "phone": "Enter a phone number using digits, spaces and + ( ) - only, up to 40 characters.",
    "choice": "Choose one of the listed options.",
}


def clean_utm(params):
    values = {}
    for key in ("utm_source", "utm_medium", "utm_campaign"):
        value = (params.get(key) or "").strip()
        if value and len(value) <= content.FIELD_LIMITS[key] and UTM_RE.match(value):
            values[key] = value
    return values


def _text(params, key):
    value = params.get(key)
    return value.strip() if isinstance(value, str) else ""


def validate_enquiry(params, interests, t=lambda text: text, lang="en_US"):
    """Return ``(payload, errors, display)``: the allowlisted payload for the
    lead, field errors keyed by field name (in the visitor's language, ``t``),
    and the values to show again."""
    limits = content.FIELD_LIMITS
    messages = {key: t(text) for key, text in MESSAGES.items()}
    errors = {}
    payload = {}

    name = _text(params, "name")
    if not 2 <= len(name) <= limits["name"]:
        errors["name"] = messages["name"]
    payload["name"] = name

    email = _text(params, "email")
    normalized = email_normalize(email) if email and len(email) <= limits["email"] else False
    if not normalized or "," in email:
        errors["email"] = messages["email"]
    payload["email"] = email

    enquiry_type = _text(params, "enquiry_type")
    if enquiry_type not in dict(content.ENQUIRY_TYPES):
        errors["enquiry_type"] = messages["enquiry_type"]
    payload["enquiry_type"] = enquiry_type

    for key in ("company", "region", "details"):
        value = _text(params, key)
        if len(value) > limits[key]:
            errors[key] = messages[key]
        payload[key] = value

    phone = _text(params, "phone")
    if len(phone) > limits["phone"] or not PHONE_RE.match(phone):
        errors["phone"] = messages["phone"]
    payload["phone"] = phone

    for key, choices in (("role", content.ROLES), ("sites", content.SITES), ("doors", content.DOORS),
                         ("connection", content.CONNECTIONS)):
        value = _text(params, key)
        if value and value not in dict(choices):
            errors[key] = messages["choice"]
        payload[key] = value

    allowed_interests = [key for key, _label in content.INTERESTS]
    if any(value not in allowed_interests for value in interests):
        errors["interests"] = messages["choice"]
    payload["interests"] = [key for key in allowed_interests if key in set(interests)]

    source_path = _text(params, "source_path")
    known = source_path in content.ROUTES or source_path.startswith((content.RESOURCE_PREFIX, content.POST_PREFIX))
    payload["source_path"] = source_path if known and len(source_path) <= 200 else "/contact"
    payload.update(clean_utm(params))

    submission_id = _text(params, "submission_id")
    if not SUBMISSION_ID_RE.match(submission_id):
        errors["form"] = t("This form has expired. Reload the page and send it again.")
    payload["submission_id"] = submission_id
    payload["lang"] = lang

    display = dict(payload)
    return payload, errors, display


class SpkWebsiteEnquiry(http.Controller):

    @http.route("/website/spk/enquiry", type="http", auth="public", website=True, methods=["POST"],
                sitemap=False)
    def enquiry(self, **post):
        if not is_v2_enabled(request.env):
            return request.not_found()
        wants_json = "application/json" in (request.httprequest.headers.get("Accept") or "")
        if is_preview(request.env):
            # A review copy never stores enquiries.
            return self._failure(wants_json, 503, "preview", {}, None)
        if (request.httprequest.content_length or 0) > MAX_BODY_BYTES:
            return self._failure(wants_json, 413, "too_large", {}, None)

        form = request.httprequest.form
        _url_code, t = _lang()
        payload, errors, display = validate_enquiry(post, form.getlist("interests"), t, request.env.lang or "en_US")
        if form.get(HONEYPOT_FIELD):
            _logger.info("Website enquiry rejected: honeypot field filled")
            return self._failure(wants_json, 400, "rejected", {}, display)
        if errors:
            return self._failure(wants_json, 400, "invalid", errors, display)

        Lead = request.env["crm.lead"]
        already_received = Lead.sudo().with_context(active_test=False).search_count(
            [("spk_submission_id", "=", payload["submission_id"])])
        if not already_received:
            remote_addr = request.httprequest.remote_addr
            if not request.env["spk.website.enquiry.attempt"]._spk_register_attempt(remote_addr):
                return self._failure(wants_json, 429, "throttled", {}, display)
            try:
                human = request.env["ir.http"]._verify_request_recaptcha_token(CAPTCHA_ACTION)
            except (UserError, ValidationError):
                human = False
            if not human:
                return self._failure(wants_json, 400, "captcha", {}, display)

        status, _lead = Lead._spk_submit_website_enquiry(payload, request.website)
        if status in (CREATED, DUPLICATE):
            request.session["spk_enquiry_received"] = payload["enquiry_type"]
            if wants_json:
                return request.make_json_response({"ok": True, "status": status})
            return request.redirect("/thank-you", code=303)
        if status == CONFLICT:
            return self._failure(wants_json, 409, "conflict", {}, display)
        return self._failure(wants_json, 503, "retry", {}, display)

    def _failure(self, wants_json, status, code, errors, display):
        if wants_json:
            return request.make_json_response({"ok": False, "error": code, "fields": errors}, status=status)
        if display is None:
            display = {}
        submission_id = display.get("submission_id") if SUBMISSION_ID_RE.match(display.get("submission_id") or "") \
            else None
        if code == "conflict":
            submission_id = None
        errors = dict(errors)
        if code != "invalid":
            errors["form"] = errors.get("form") or "send"
        return render_contact(display, errors=errors, status=status, submission_id=submission_id)
