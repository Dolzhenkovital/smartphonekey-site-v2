# -*- coding: utf-8 -*-
"""Website 2.0 enquiries as CRM leads.

The contact form's context (enquiry type, role, sites, doors, connection,
interests, the page it came from) is kept on the lead in typed fields. The
submission ID makes the form idempotent: the same ID with the same payload
answers the original success without a second lead, enforced by a unique
index rather than a search-then-create race.
"""

import hashlib
import json
import logging

import psycopg2.errors

from odoo import SUPERUSER_ID, api, fields, models
from odoo.tools import plaintext2html

from ..site_content import CONNECTIONS, DOORS, ENQUIRY_TYPES, INTERESTS, ROLES, SITES

_logger = logging.getLogger(__name__)

CREATED, DUPLICATE, CONFLICT, RETRY = "created", "duplicate", "conflict", "retry"


def enquiry_digest(payload):
    """A fingerprint of everything the visitor sent except the submission ID."""
    body = {key: value for key, value in payload.items() if key != "submission_id"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class CrmLead(models.Model):
    _inherit = "crm.lead"

    spk_enquiry_type = fields.Selection(list(ENQUIRY_TYPES), string="Website enquiry", readonly=True)
    spk_role = fields.Selection(list(ROLES), string="Visitor role", readonly=True)
    spk_sites = fields.Selection(list(SITES), string="Sites", readonly=True)
    spk_doors = fields.Selection(list(DOORS), string="Doors", readonly=True)
    spk_connection = fields.Selection(list(CONNECTIONS), string="Connection", readonly=True)
    spk_interests = fields.Char("Interests", readonly=True)
    spk_region = fields.Char("Country or region", readonly=True)
    spk_source_path = fields.Char("Website page", readonly=True)
    spk_utm_source = fields.Char("UTM source", readonly=True)
    spk_utm_medium = fields.Char("UTM medium", readonly=True)
    spk_utm_campaign = fields.Char("UTM campaign", readonly=True)
    spk_submission_id = fields.Char("Submission ID", readonly=True, copy=False, index=True)
    spk_submission_digest = fields.Char(readonly=True, copy=False)

    _sql_constraints = [
        ("spk_submission_id_unique", "unique(spk_submission_id)",
         "This website enquiry has already been received."),
    ]

    @api.model
    def _spk_submit_website_enquiry(self, payload, website):
        """Create the lead for a validated enquiry, once.

        ``payload`` holds only allowlisted, validated values (see
        controllers/enquiry.py). Returns ``(status, lead)``: ``created`` with
        the new lead, ``duplicate`` when this submission already became a lead,
        ``conflict`` when its ID arrived again with different content, and
        ``retry`` when a concurrent request owns the ID but its outcome cannot
        be read yet. The lead is never handed back to the visitor.
        """
        Lead = self.sudo().with_context(active_test=False)
        digest = enquiry_digest(payload)
        existing = Lead.search([("spk_submission_id", "=", payload["submission_id"])], limit=1)
        if existing:
            return (DUPLICATE if existing.spk_submission_digest == digest else CONFLICT), existing
        values = self._spk_enquiry_lead_values(payload, website, digest)
        try:
            with self.env.cr.savepoint():
                lead = Lead.create(values)
                lead.flush_recordset()
        except psycopg2.errors.UniqueViolation:
            # A concurrent request committed this submission between our search
            # and our insert; our snapshot cannot see it, a fresh one can.
            committed = self._spk_committed_enquiry_digest(payload["submission_id"])
            if committed is None:
                return RETRY, Lead
            return (DUPLICATE if committed == digest else CONFLICT), Lead
        _logger.info("Website enquiry %s (%s) created lead %s",
                     payload["submission_id"], payload["enquiry_type"], lead.id)
        return CREATED, lead

    @api.model
    def _spk_committed_enquiry_digest(self, submission_id):
        with self.env.registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            lead = env["crm.lead"].with_context(active_test=False).search(
                [("spk_submission_id", "=", submission_id)], limit=1)
            return lead.spk_submission_digest if lead else None

    @api.model
    def _spk_enquiry_lead_values(self, payload, website, digest):
        types = dict(ENQUIRY_TYPES)
        labels = {
            "role": dict(ROLES), "sites": dict(SITES), "doors": dict(DOORS),
            "connection": dict(CONNECTIONS),
        }
        interest_labels = dict(INTERESTS)
        who = payload.get("company") or payload["name"]
        lines = ["Website enquiry: %s" % types[payload["enquiry_type"]]]
        for key, title in (("role", "Role"), ("sites", "Sites"), ("doors", "Doors"), ("connection", "Connection")):
            if payload.get(key):
                lines.append("%s: %s" % (title, labels[key][payload[key]]))
        if payload.get("interests"):
            lines.append("Interests: %s" % ", ".join(interest_labels[key] for key in payload["interests"]))
        if payload.get("region"):
            lines.append("Country or region: %s" % payload["region"])
        lines.append("Page: %s" % payload["source_path"])
        if payload.get("details"):
            lines += ["", payload["details"]]
        values = {
            "name": "Website — %s — %s" % (types[payload["enquiry_type"]], who),
            "contact_name": payload["name"],
            "email_from": payload["email"],
            "partner_name": payload.get("company") or False,
            "phone": payload.get("phone") or False,
            # plaintext2html escapes the visitor's text: it is stored, never executed.
            "description": plaintext2html("\n".join(lines)),
            # Server-owned routing: the website's sales team, salesperson and
            # company. An explicit (possibly empty) salesperson keeps the
            # public user off the lead.
            "team_id": website.crm_default_team_id.id,
            "user_id": website.crm_default_user_id.id,
            "company_id": website.company_id.id,
            "spk_enquiry_type": payload["enquiry_type"],
            "spk_role": payload.get("role") or False,
            "spk_sites": payload.get("sites") or False,
            "spk_doors": payload.get("doors") or False,
            "spk_connection": payload.get("connection") or False,
            "spk_interests": ",".join(payload.get("interests") or ()) or False,
            "spk_region": payload.get("region") or False,
            "spk_source_path": payload["source_path"],
            "spk_utm_source": payload.get("utm_source") or False,
            "spk_utm_medium": payload.get("utm_medium") or False,
            "spk_utm_campaign": payload.get("utm_campaign") or False,
            "spk_submission_id": payload["submission_id"],
            "spk_submission_digest": digest,
        }
        medium = self.env.ref("utm.utm_medium_website", raise_if_not_found=False)
        if medium:
            values["medium_id"] = medium.id
        return values
