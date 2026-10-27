# -*- coding: utf-8 -*-
"""Rendering helpers shared by the controllers and the 404 handler: the
values every 2.0 page gets (navigation, metadata, canonical URL, languages,
structured data, preview flags) and the switches that control the site.

Languages: Odoo's website routing puts the visitor's language in the URL
(/fr/..., /de/..., /es/..., /uk/...) and in ``request.lang``. Template text and
the translatable fields of the content records come from the module's .po
files the usual way; the English strings of site_content.py are translated
here, from the same .po files (Python code terms).
"""

import json
from types import SimpleNamespace

from babel.dates import format_date
from lxml import etree, html as lxml_html
from markupsafe import Markup

from odoo.http import request
from odoo.modules.module import get_manifest
from odoo.tools import str2bool
from odoo.tools.translate import code_translations

from odoo.addons.spk_website.controllers.main import _template_values as baseline_template_values

from . import site_content as content

# The site data as templates see it: QWeb refuses a module in its context.
SITE_DATA = SimpleNamespace(**{name: value for name, value in vars(content).items() if name.isupper()})
LANGS = {odoo_code: (url_code, odoo_code, name) for url_code, odoo_code, name in content.SITE_LANGS}
DEFAULT = LANGS["en_US"]
SOFT_HYPHEN = "\u00ad"  # the translations break long words at it (tools/i18n_soft_hyphens.py)

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


# --- Languages ----------------------------------------------------------------

def current_lang():
    """``((url code, Odoo code, name), supported)`` for this request. A website
    language the 2.0 site has no copy for shows the English text, noindex."""
    lang = getattr(request, "lang", None)
    code = lang.code if lang else (request.env.lang or "en_US")
    return LANGS.get(code, DEFAULT), code in LANGS


def translator(odoo_code):
    """``t(text, **kw)``: a site_content string in the language ``odoo_code``."""
    catalogue = {} if odoo_code == "en_US" else code_translations.get_python_translations("spk_website_v2", odoo_code)

    def t(text, **kwargs):
        value = catalogue.get(text) or text
        return value % kwargs if kwargs else value
    return t


def localized_data(t):
    """SITE_DATA with every label the pages show in the visitor's language."""
    data = dict(vars(SITE_DATA))
    for name in ("ENQUIRY_TYPES", "ROLES", "SITES", "DOORS", "CONNECTIONS", "INTERESTS", "HOME_SITE_CHOICES",
                 "SETUP_ROLES", "SETUP_INTERESTS"):
        data[name] = tuple((key, t(label)) for key, label in getattr(content, name))
    for name in ("HOME_SITE_COPY", "HOME_CONNECTION_COPY", "SETUP_CONNECTION_ADVICE"):
        data[name] = {key: t(text) for key, text in getattr(content, name).items()}
    data["INSTRUCTION_PATHS"] = {path: t(label) for path, label in content.INSTRUCTION_PATHS.items()}
    return SimpleNamespace(**data)


def switch_url(path, code):
    """The switcher's link. English goes through /en/...: Odoo answers it with a
    redirect to the plain URL and resets the remembered language, which a plain
    URL would otherwise send back to the visitor's last language."""
    if code == content.DEFAULT_LANG:
        return "/" + code + ("" if path == "/" else path)
    return content.lang_url(path, code)


def localized_menu(menu, t):
    return tuple((t(group), tuple((t(label), path) for label, path in links)) for group, links in menu)


# Babel locale for the long date of each site language: British English for the
# English pages ("27 October 2026"); the other languages use their own long
# format ("27. Oktober 2026", "27 de octubre de 2026", "27 жовтня 2026 р.").
DATE_LOCALES = {"en_US": "en_GB"}


def day_formatter(odoo_code):
    """27 October 2026, 27 octobre 2026, 27. Oktober 2026, 27 de octubre de 2026, 27 жовтня 2026 р."""
    locale = DATE_LOCALES.get(odoo_code, odoo_code)

    def format_day(value):
        return format_date(value, format="long", locale=locale) if value else ""
    return format_day


def json_for_script(data):
    """JSON safe inside a <script> element."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return Markup(text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def crumbs_for(path, route, t):
    if path == "/":
        return []
    trail = [(t("Home"), "/")]
    for parent in route.get("crumbs", ()):
        trail.append((t(content.ROUTES[parent]["label"]), parent))
    trail.append((route["label"], path))
    return trail


def structured_data(page_url, route, crumbs, url_code, article=None):
    """The page's JSON-LD graph, built from the same values the page shows."""
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
            "inLanguage": [lang[0] for lang in content.SITE_LANGS],
            "publisher": {"@id": content.ORGANIZATION_ID},
        })
    page = {
        "@type": page_types.get(route.get("kind"), "WebPage"),
        "@id": page_url + "#webpage",
        "url": page_url,
        "name": route["title"],
        "description": route["description"],
        "inLanguage": url_code,
        "isPartOf": {"@id": content.WEBSITE_ID},
    }
    if crumbs:
        page["breadcrumb"] = {"@id": page_url + "#breadcrumb"}
    graph.append(page)
    if crumbs:
        graph.append({
            "@type": "BreadcrumbList",
            "@id": page_url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": index, "name": label,
                 "item": content.ORIGIN + content.lang_url(crumb_path, url_code)}
                for index, (label, crumb_path) in enumerate(crumbs, start=1)
            ],
        })
    if article:
        author = ({"@type": "Person", "name": article["author_name"]} if article["kind"] == "post"
                  else {"@type": "Organization", "name": article["author_name"], "url": content.ORIGIN + "/about"})
        node = {
            "@type": "Article",
            "@id": page_url + "#article",
            "headline": article["name"].replace(SOFT_HYPHEN, ""),  # no soft hyphens in data
            "description": article["description"],
            "datePublished": article["published_on"].isoformat(),
            "dateModified": (article["modified_on"] or article["published_on"]).isoformat(),
            "author": author,
            "publisher": {"@id": content.ORGANIZATION_ID},
            "mainEntityOfPage": {"@id": page_url + "#webpage"},
            "inLanguage": "en" if article["kind"] == "post" else url_code,
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


def page_values(path, route=None, article=None, english_only=False, **extra):
    """Everything layout.xml needs, plus the page's own values.

    ``english_only``: a page kept in English in every language (legal text,
    archived articles). Its canonical URL is the English one, without
    language alternates."""
    env = request.env
    (url_code, odoo_code, _name), supported = current_lang()
    t = translator(odoo_code)
    route = route or content.ROUTES[path]
    route = dict(route, title=t(route["title"]), description=t(route["description"]), label=t(route["label"]))
    english_only = english_only or path in content.ENGLISH_ONLY
    # A response that is not a real document (the 404) sets route["canonical"] = False: no canonical link,
    # no og:url, no breadcrumb and no structured data. route["breadcrumbs"] = False drops only the trail
    # (a confirmation page that shows none).
    has_canonical = route.get("canonical", True)
    crumbs = crumbs_for(path, route, t) if has_canonical and route.get("breadcrumbs", True) else []
    noindex = (not route.get("index", True)) or is_noindex_environment(env) or not supported
    localized = not english_only and supported
    page_url = content.ORIGIN + (content.lang_url(path, url_code) if localized else path)
    alternates = []
    if localized and not noindex:
        alternates = [(code, content.ORIGIN + content.lang_url(path, code)) for code, _odoo, _n in content.SITE_LANGS]
        alternates.append(("x-default", content.ORIGIN + path))
    image = route.get("image") or content.OG_IMAGE
    values = baseline_template_values()
    values.update({
        "content": localized_data(t),
        "t": t,
        "page_path": path,
        "route": route,
        "title": route["title"],
        "page_description": route["description"],
        "canonical": page_url if has_canonical else None,
        "alternates": alternates,
        "lang_code": url_code,
        "og_locale": content.OG_LOCALES[url_code],
        "lang_switch": [(name, switch_url(path, code), code, code == url_code)
                        for code, _odoo, name in content.SITE_LANGS],
        "current_lang_name": LANGS[odoo_code][2] if supported else DEFAULT[2],
        "english_only": english_only and url_code != content.DEFAULT_LANG,
        "robots": "noindex, nofollow" if noindex else False,
        "og_image": dict(image, url=content.ORIGIN + image["path"]),
        "crumbs": crumbs,
        "jsonld": (structured_data(page_url, route, crumbs, url_code if localized else "en", article=article)
                   if has_canonical else ""),
        "nav": localized_menu(content.NAV, t),
        "footer_nav": localized_menu(content.FOOTER, t),
        "preview_mode": is_preview(env),
        "contact_email": content.CONTACT_EMAIL,
        "v2_asset_version": get_manifest("spk_website_v2").get("version", ""),
        "nav_current": content.route_path(path),
        "format_day": day_formatter(odoo_code),
    })
    values.update(extra)
    return values


def render_page(path, route=None, status=200, article=None, english_only=False, **extra):
    values = page_values(path, route=route, article=article, english_only=english_only, **extra)
    headers = [("Content-Language", values["lang_code"])]
    if values["robots"]:
        headers.append(("X-Robots-Tag", "noindex, nofollow"))
    return request.render(route["template"] if route else content.ROUTES[path]["template"], values,
                          status=status, headers=headers)
