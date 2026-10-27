# -*- coding: utf-8 -*-
"""smartphonekey.com 2.0: public pages, the Webflow URLs it takes over,
sitemap and robots.

Extends the AP-428 baseline (``spk_website``) instead of replacing it: the
home page keeps the AP-429 "Use SmartphoneKey site as homepage" switch, the
baseline's own routes answer every URL this module does not claim (the
portal entry ``/adminpanel``, the noindex ``/referral-program``, its form
endpoint), and ``spk_website_v2.enabled`` set to "False" hands everything
back to the baseline site without touching data.
"""

import uuid
from urllib.parse import urlsplit

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request

from odoo.addons.spk_website.controllers.main import SpkWebsite, SpkWebsiteHome, is_homepage_enabled

from .. import setup_guide
from .. import site_content as content
from ..rendering import (
    booking_url, current_lang, is_noindex_environment, is_v2_enabled, json_for_script, prepare_body, render_page,
    translator,
)

# Private or transactional routes crawlers have no reason to fetch. Robots is
# not access control: these routes keep their own authentication. The asset
# bundles under /web/assets stay crawlable so pages render for search engines.
PRIVATE_PREFIXES = ("/my", "/odoo", "/web/login", "/web/signup", "/web/reset_password",
                    "/website/spk/", "/spk-website/")


def _lang():
    """(url code, translator) of the current request."""
    (url_code, odoo_code, _name), _supported = current_lang()
    return url_code, translator(odoo_code)


def _require_v2():
    if not is_v2_enabled(request.env):
        raise NotFound()


def _source_path():
    """The site page the visitor came from, if it is one of ours."""
    referrer = urlsplit(request.httprequest.referrer or "")
    if referrer.netloc and referrer.netloc != request.httprequest.host:
        return "/contact"
    path = content.route_path(referrer.path or "")
    known = path in content.ROUTES or path.startswith((content.RESOURCE_PREFIX, content.POST_PREFIX))
    return path if known and path != "/thank-you" else "/contact"


def contact_defaults(query):
    """Contact form values from the query string: enums and campaign tags only."""
    from .enquiry import clean_utm
    interest = content.INTEREST_PARAM.get(query.get("interest"))
    enquiry_type, interests = interest or (None, ())
    if query.get("enquiry_type") in dict(content.ENQUIRY_TYPES):
        enquiry_type = query["enquiry_type"]
    allowed = {
        "role": dict(content.ROLES), "sites": dict(content.SITES), "doors": dict(content.DOORS),
        "connection": dict(content.CONNECTIONS),
    }
    values = {field: query.get(field) for field in allowed if query.get(field) in allowed[field]}
    listed = set(request.httprequest.args.getlist("interests"))
    chosen = set(interests) | listed
    values["interests"] = [key for key, _label in content.INTERESTS if key in chosen]
    values["enquiry_type"] = enquiry_type or ""
    values.update(clean_utm(query))
    # The page shows its "answers from the site recommendations" note only when
    # enum choices of that tool arrived. ``?interest=automation`` ticks an
    # interest too, but that comes from a link on the site, not from the tool.
    values["prefilled"] = bool(
        any(field in values for field in allowed)
        or listed.intersection(key for key, _label in content.INTERESTS))
    return values


class SpkWebsiteV2Home(SpkWebsiteHome):

    @http.route()
    def index(self, **kw):
        homepage_url = request.website._get_cached("homepage_url")
        if not is_v2_enabled(request.env) or not is_homepage_enabled(request.env) \
                or (homepage_url and homepage_url != "/"):
            return super().index(**kw)
        url_code, t = _lang()
        return render_page("/", setup_rules=json_for_script(setup_guide.rules_for_script(t, url_code)))

    @http.route()
    def robots(self, **kwargs):
        if not is_v2_enabled(request.env):
            return super().robots(**kwargs)
        website = request.website
        url_root = request.httprequest.url_root
        if is_noindex_environment(request.env) or (website.domain and not website._is_indexable_url(url_root)):
            lines = ["User-agent: *", "Disallow: /"]
        else:
            # Search crawlers and every other agent share one group, so no
            # bot-specific group can lose the private-route exclusions. Training
            # crawlers are not singled out: the owner's policy is whatever the
            # website's own robots.txt setting adds below.
            lines = ["User-agent: *"] + ["Disallow: %s" % prefix for prefix in PRIVATE_PREFIXES]
            lines += ["", "Sitemap: %s/sitemap.xml" % (website.domain or url_root.rstrip("/"))]
            custom = (website.sudo().robots_txt or "").strip()
            if custom:
                lines += ["", "# Website settings", custom]
        return request.make_response("\n".join(lines) + "\n", headers=[("Content-Type", "text/plain")])

    @http.route()
    def sitemap_xml_index(self, **kwargs):
        if not is_v2_enabled(request.env):
            return super().sitemap_xml_index(**kwargs)
        root = (request.website.domain or request.httprequest.url_root).rstrip("/")
        codes = [code for code, _odoo, _name in content.SITE_LANGS]
        entries = []

        def add(path, lastmod, translated=True):
            # Every language copy is listed; English-only pages once.
            for code in (codes if translated else [content.DEFAULT_LANG]):
                entries.append((content.lang_url(path, code), lastmod))

        for path in content.public_paths():
            route = content.ROUTES[path]
            add(path, route.get("lastmod", content.EDITORIAL_DATE), path not in content.ENGLISH_ONLY)
        Resource = request.env["spk.website.resource"]
        for kind in ("guide", "post"):
            for resource in Resource._public_list(kind):
                modified = resource["modified_on"] or resource["published_on"]
                add(resource["path"], modified.isoformat(), kind == "guide")
        for member in request.env["spk.website.team.member"]._public_list():
            add(content.TEAM_PREFIX + member["slug"], None, translated=False)
        if request.env["ir.module.module"].sudo().search_count(
                [("name", "=", "smartphonekey"), ("state", "=", "installed")]):
            entries += [(path, None) for path in content.INSTRUCTION_PATHS]
        body = ['<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for path, lastmod in entries:
            body.append("  <url><loc>%s%s</loc>%s</url>" % (
                root, path, "<lastmod>%s</lastmod>" % lastmod if lastmod else ""))
        body.append("</urlset>")
        return request.make_response("\n".join(body) + "\n",
                                     headers=[("Content-Type", "application/xml;charset=utf-8")])


class SpkWebsiteV2Legacy(SpkWebsite):
    """The Webflow URLs: retained in the 2.0 shell or permanently redirected."""

    @http.route(sitemap=False)
    def page(self, **kw):
        if not is_v2_enabled(request.env):
            return super().page(**kw)
        path = request.httprequest.path
        action, target = content.LEGACY_ROUTES.get(path, ("baseline", None))
        if action == "redirect":
            return request.redirect(target, code=301)
        if action == "retain" and path == "/contact":
            return render_contact(contact_defaults(request.httprequest.args), errors={})
        if action == "retain" and path in content.ROUTES:
            return render_page(path)
        return super().page(**kw)

    @http.route(sitemap=False)
    def post(self, slug, **kw):
        if not is_v2_enabled(request.env):
            return super().post(slug, **kw)
        article = request.env["spk.website.resource"]._public_resource("post", slug)
        if not article:
            raise NotFound()
        return _render_article(article, ("/resources",), english_only=True)

    @http.route(sitemap=False)
    def team_member(self, slug, **kw):
        if not is_v2_enabled(request.env):
            return super().team_member(slug, **kw)
        member = request.env["spk.website.team.member"]._public_member(slug)
        if not member:
            raise NotFound()
        _url_code, t = _lang()
        route = {
            "template": "spk_website_v2.page_team_member",
            "title": t("%(name)s, %(job)s | SmartphoneKey", name=member["name"], job=member["job_title"]),
            "description": t("Profile of %(name)s, %(job)s, on the SmartphoneKey website.", name=member["name"], job=member["job_title"]),
            "label": member["name"],
            "kind": "webpage",
            "crumbs": ("/about",),
        }
        # The biographies are kept in English; the About page lists translated roles.
        return render_page(content.TEAM_PREFIX + slug, route=route, member=member, english_only=True)

    @http.route()
    def page_not_found(self, **kw):
        if not is_v2_enabled(request.env):
            return super().page_not_found(**kw)
        return render_not_found()


def render_not_found():
    _url_code, t = _lang()
    route = {
        "template": "spk_website_v2.page_404",
        "title": t("Page not found | SmartphoneKey"),
        "description": t("The page you asked for is not on the SmartphoneKey website."),
        "label": t("Page not found"),
        "kind": "webpage",
        "index": False,
        "canonical": False,
        "crumbs": (),
    }
    return render_page(request.httprequest.path, route=route, status=404)


def _render_article(article, parents, english_only=False):
    route = {
        "template": "spk_website_v2.page_article",
        "title": article["seo_title"],
        "description": article["description"],
        "label": article["name"],
        "kind": "article",
        "crumbs": parents,
    }
    body, contents = prepare_body(article["body"])
    article = dict(article, body=body, contents=contents)
    return render_page(article["path"], route=route, article=article, resource=article, english_only=english_only)


class SpkWebsiteV2(http.Controller):

    @http.route(["/platform", "/platform/access-management", "/platform/automation", "/platform/visitor-access",
                 "/solutions/property-managers", "/solutions/integrators", "/products/readers", "/security",
                 "/about"], type="http", auth="public", website=True, sitemap=False)
    def static_page(self, **kw):
        _require_v2()
        path = request.httprequest.path
        extra = {}
        if path == "/about":
            extra["team"] = request.env["spk.website.team.member"]._public_list()
        return render_page(path, **extra)

    @http.route("/products/smartphonekey-reader-1", type="http", auth="public", website=True, sitemap=False)
    def old_reader_page(self, **kw):
        """Linked from three Webflow articles but never published there (a 404)."""
        _require_v2()
        return request.redirect("/products/readers", code=301)

    @http.route("/compatibility", type="http", auth="public", website=True, sitemap=False)
    def compatibility(self, **kw):
        _require_v2()
        Rows = request.env["spk.website.compatibility"]
        return render_page("/compatibility", rows={
            category: Rows._public_rows(category) for category in ("cards", "digital", "matter", "network", "cameras")
        }, reviewed_on=Rows._public_reviewed_on())

    @http.route("/resources", type="http", auth="public", website=True, sitemap=False)
    def resources(self, **kw):
        _require_v2()
        _url_code, t = _lang()
        Resource = request.env["spk.website.resource"]
        guides = Resource._public_list("guide")
        groups = []
        for key, label in content.GUIDE_GROUPS:
            groups.append((key, t(label), [guide for guide in guides if guide["category"] == key]))
        return render_page("/resources", guide_groups=groups, posts=Resource._public_list("post"))

    @http.route("/resources/<string:slug>", type="http", auth="public", website=True, sitemap=False)
    def resource(self, slug, **kw):
        _require_v2()
        article = request.env["spk.website.resource"]._public_resource("guide", slug)
        if not article:
            raise NotFound()
        return _render_article(article, ("/resources",))

    @http.route("/find-your-setup", type="http", auth="public", website=True, sitemap=False)
    def find_your_setup(self, **kw):
        _require_v2()
        url_code, t = _lang()
        args = request.httprequest.args
        selection = setup_guide.clean_selection(args, args.getlist("interests"))
        mapped = content.HOME_SITE_TO_SETUP.get(args.get("site"))
        if mapped and not any(field in selection for field in ("role", "sites", "doors")):
            # The home hero's compact tool hands over its two choices: the site choice
            # becomes the matching role or number of sites, next to the connection.
            selection = setup_guide.clean_selection(
                dict(mapped, connection=selection.get("connection")), selection.get("interests", ()))
        return render_page("/find-your-setup", selection=selection, result=setup_guide.result_for(selection, t),
                           setup_rules=json_for_script(setup_guide.rules_for_script(t, url_code)),
                           setup_fields=setup_guide.FIELDS)

    @http.route("/thank-you", type="http", auth="public", website=True, sitemap=False)
    def thank_you(self, **kw):
        _require_v2()
        received = request.session.pop("spk_enquiry_received", None)
        return render_page("/thank-you", received=received in dict(content.ENQUIRY_TYPES),
                           booking_url=booking_url(request.env))


def render_contact(values, errors, status=200, submission_id=None):
    form = dict(values)
    prefilled = bool(form.pop("prefilled", False))
    form.setdefault("interests", [])
    form["submission_id"] = submission_id or uuid.uuid4().hex
    form["source_path"] = form.get("source_path") or _source_path()
    return render_page("/contact", status=status, form=form, errors=errors, prefilled=prefilled,
                       booking_url=booking_url(request.env))
