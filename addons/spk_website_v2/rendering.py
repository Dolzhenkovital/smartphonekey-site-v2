# -*- coding: utf-8 -*-
"""Rendering helpers shared by the controllers and the 404 handler: the
values every 2.0 page gets (navigation, metadata, canonical URL, structured
data, preview flags) and the switches that control the site."""

import json
from types import SimpleNamespace

from lxml import etree, html as lxml_html
from markupsafe import Markup

from odoo.http import request
from odoo.modules.module import get_manifest
from odoo.tools import str2bool

from odoo.addons.spk_website.controllers.main import _template_values as baseline_template_values

from . import site_content as content

# The site data as templates see it: QWeb refuses a module in its context.
SITE_DATA = SimpleNamespace(**{name: value for name, value in vars(content).items() if name.isupper()})

# Rollback switch: "False" hands every URL back to the AP-428 site. Stored as
# text and on when missing, like the baseline's homepage switch (a parameter
# set to False is deleted by ir.config_parameter.set_param()).
ENABLED_PARAM = "spk_website_v2.enabled"
# A review copy (the GitHub Pages export, a protected stage): noindex, a
# visible banner, and the enquiry form does not send anything.
PREVIEW_PARAM = "spk_website_v2.preview_mode"
# Optional follow-up link after a successful enquiry; only HTTPS on an allowed host.
BOOKING_URL_PARAM = "spk_website_v2.booking_url"
BOOKING_HOSTS_PARAM = "spk_website_v2.booking_hosts"


def _param(env, key, default=""):
    return env["ir.config_parameter"].sudo().get_param(key) or default


def is_v2_enabled(env):
    return str2bool(_param(env, ENABLED_PARAM, "True"), True)


def is_preview(env):
    return str2bool(_param(env, PREVIEW_PARAM, "False"), False)


def is_noindex_environment(env):
    """A review copy or a neutralized database (Odoo.sh staging) is never indexed."""
    neutralized = str2bool(_param(env, "database.is_neutralized", "False"), False)
    return is_preview(env) or neutralized


def booking_url(env):
    from urllib.parse import urlsplit
    url = _param(env, BOOKING_URL_PARAM).strip()
    hosts = {host.strip().lower() for host in _param(env, BOOKING_HOSTS_PARAM, "cal.com").split(",") if host.strip()}
    parts = urlsplit(url)
    if parts.scheme == "https" and parts.hostname and parts.hostname.lower() in hosts:
        return url
    return False


def format_day(value):
    """26 October 2026: the date style the pages use."""
    return "%d %s" % (value.day, value.strftime("%B %Y")) if value else ""


def json_for_script(data):
    """JSON safe inside a <script> element."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return Markup(text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def crumbs_for(path, route):
    if path == "/":
        return []
    trail = [("Home", "/")]
    for parent in route.get("crumbs", ()):
        trail.append((content.ROUTES[parent]["label"], parent))
    trail.append((route["label"], path))
    return trail


def structured_data(path, route, crumbs, article=None):
    """The page's JSON-LD graph, built from the same values the page shows."""
    canonical = content.canonical_url(path)
    page_types = {"home": "WebPage", "collection": "CollectionPage", "contact": "ContactPage", "about": "AboutPage"}
    graph = []
    if route.get("kind") == "home":
        graph.append({
            "@type": "Organization",
            "@id": content.ORGANIZATION_ID,
            "name": "SmartphoneKey",
            "url": content.ORIGIN + "/",
            "logo": {"@type": "ImageObject", "url": content.ORIGIN + content.LOGO_PATH},
            "email": content.CONTACT_EMAIL,
            "sameAs": list(content.SAME_AS),
        })
        graph.append({
            "@type": "WebSite",
            "@id": content.WEBSITE_ID,
            "url": content.ORIGIN + "/",
            "name": "SmartphoneKey",
            "inLanguage": "en",
            "publisher": {"@id": content.ORGANIZATION_ID},
        })
    page = {
        "@type": page_types.get(route.get("kind"), "WebPage"),
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": route["title"],
        "description": route["description"],
        "inLanguage": "en",
        "isPartOf": {"@id": content.WEBSITE_ID},
    }
    if crumbs:
        page["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    graph.append(page)
    if crumbs:
        graph.append({
            "@type": "BreadcrumbList",
            "@id": canonical + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": index, "name": label, "item": content.canonical_url(crumb_path)}
                for index, (label, crumb_path) in enumerate(crumbs, start=1)
            ],
        })
    if article:
        author = ({"@type": "Person", "name": article["author_name"]} if article["kind"] == "post"
                  else {"@type": "Organization", "name": article["author_name"], "url": content.ORIGIN + "/about"})
        node = {
            "@type": "Article",
            "@id": canonical + "#article",
            "headline": article["name"],
            "description": article["description"],
            "datePublished": article["published_on"].isoformat(),
            "dateModified": (article["modified_on"] or article["published_on"]).isoformat(),
            "author": author,
            "publisher": {"@id": content.ORGANIZATION_ID},
            "mainEntityOfPage": {"@id": canonical + "#webpage"},
            "inLanguage": "en",
        }
        if article.get("hero_image"):
            node["image"] = content.ORIGIN + article["hero_image"]
        graph.append(node)
    return json_for_script({"@context": "https://schema.org", "@graph": graph})


# Placeholders an editor can put in a resource body: replaced by a shared
# template so a table maintained in one place appears on several pages.
BODY_COMPONENTS = {
    "spk-component-reader-comparison": "spk_website_v2.reader_comparison",
}


def prepare_body(body):
    """Editor HTML made ready for the page: shared components rendered, every
    table in a labelled scroll region, images lazy, every section heading
    anchored. Returns ``(html, contents)`` with contents as (id, title) pairs."""
    if not body:
        return body, []
    fragment = lxml_html.fragment_fromstring(str(body), create_parent="div")
    for css_class, template in BODY_COMPONENTS.items():
        for placeholder in fragment.xpath("//*[contains(concat(' ', @class, ' '), ' %s ')]" % css_class):
            rendered = request.env["ir.ui.view"]._render_template(template, {})
            for node in lxml_html.fragments_fromstring(str(rendered)):
                if isinstance(node, str):
                    continue
                placeholder.addprevious(node)
            placeholder.getparent().remove(placeholder)
    for index, table in enumerate(fragment.iter("table"), start=1):
        if table.getparent().get("class") == "spk-table":
            continue
        caption = table.find("caption")
        label = caption.text_content().strip() if caption is not None else "Table %d" % index
        region = etree.Element("div", {"class": "spk-table", "role": "region", "tabindex": "0", "aria-label": label})
        table.addprevious(region)
        region.append(table)
    for image in fragment.iter("img"):
        image.set("loading", "lazy")
        image.set("decoding", "async")
    contents = []
    for index, heading in enumerate(fragment.iter("h2"), start=1):
        anchor = heading.get("id") or "section-%d" % index
        heading.set("id", anchor)
        contents.append((anchor, heading.text_content().strip()))
    inner = "".join(lxml_html.tostring(child, encoding="unicode") for child in fragment)
    return Markup((fragment.text or "") + inner), contents


def page_values(path, route=None, article=None, **extra):
    """Everything layout.xml needs, plus the page's own values."""
    env = request.env
    route = route or content.ROUTES[path]
    crumbs = crumbs_for(path, route)
    noindex = (not route.get("index", True)) or is_noindex_environment(env)
    image = route.get("image") or content.OG_IMAGE
    values = baseline_template_values()
    values.update({
        "content": SITE_DATA,
        "page_path": path,
        "route": route,
        "title": route["title"],
        "page_description": route["description"],
        "canonical": content.canonical_url(path),
        "robots": "noindex, nofollow" if noindex else False,
        "og_image": dict(image, url=content.ORIGIN + image["path"]),
        "crumbs": crumbs,
        "jsonld": structured_data(path, route, crumbs, article=article),
        "nav": content.NAV,
        "footer_nav": content.FOOTER,
        "cta": content.CTA,
        "preview_mode": is_preview(env),
        "contact_email": content.CONTACT_EMAIL,
        "v2_asset_version": get_manifest("spk_website_v2").get("version", ""),
        "nav_current": content.route_path(path),
        "format_day": format_day,
    })
    values.update(extra)
    return values


def render_page(path, route=None, status=200, article=None, **extra):
    values = page_values(path, route=route, article=article, **extra)
    headers = [("X-Robots-Tag", "noindex, nofollow")] if values["robots"] else []
    return request.render(route["template"] if route else content.ROUTES[path]["template"], values,
                          status=status, headers=headers)
