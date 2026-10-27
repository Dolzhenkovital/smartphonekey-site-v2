#!/usr/bin/env python3
"""Export the Odoo-rendered 2.0 site as a static review copy (GitHub Pages).

Every page is fetched from a running test instance with
``spk_website_v2.preview_mode`` on, so the copy is the real QWeb output: same
templates, same CSS bundle, same scripts, plus the preview banner, noindex and
a contact form that never sends. The export then:

* saves each page as <path>/index.html under the Pages base path,
* rewrites site links to that base, and links to routes this module does not
  serve (the instruction site, the portal entry) to the Odoo host serving them,
* copies the CSS bundle, scripts, images and documents the pages use,
* writes the permanent redirects as small noindex pages (static hosting cannot
  answer a real 301; the Odoo module does),
* drops Odoo's per-session CSRF script and token.

    python export_static.py --odoo http://127.0.0.1:8069 --out ../preview \
        --base /smartphonekey-site-v2 --external https://spkey.odoo.com
"""

import argparse
import importlib.util
import json
import re
import shutil
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from lxml import etree, html as lxml_html

# The module's site data is plain Python: load it without importing Odoo.
_spec = importlib.util.spec_from_file_location(
    "site_content", Path(__file__).resolve().parents[1] / "addons/spk_website_v2/site_content.py")
content = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(content)

URL_ATTRIBUTES = ("href", "src", "action")
EXTRA_PAGES = ("/thank-you",)


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "spk-static-export"})
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def page_paths(odoo):
    status, body = fetch(odoo + "/sitemap.xml")
    if status != 200:
        raise SystemExit("sitemap.xml answered %s" % status)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths = [urlsplit(loc).path or "/" for loc in etree.fromstring(body).xpath("//s:loc/text()", namespaces=namespace)]
    codes = [code for code, _odoo, _name in content.SITE_LANGS]
    pages = []
    for path in paths + list(EXTRA_PAGES):
        if path in content.INSTRUCTION_PATHS:
            continue
        # English-only pages are listed once in the sitemap, but every language's
        # navigation links to its own copy of them: export those too.
        variants = [path] if path.split("/")[1:2] and path.split("/")[1] in codes else             [content.lang_url(path, code) for code in codes]
        pages += [variant for variant in variants if variant not in pages]
    return pages


class Rewriter:
    def __init__(self, base, pages, external):
        self.base = base.rstrip("/")
        self.pages = set(pages)
        self.external = external.rstrip("/")
        self.assets = set()

    def url(self, value):
        if not value.startswith("/") or value.startswith("//"):
            return value
        parts = urlsplit(value)
        path = parts.path or "/"
        suffix = ("?" + parts.query if parts.query else "") + ("#" + parts.fragment if parts.fragment else "")
        if path == "/" + content.DEFAULT_LANG or path.startswith("/%s/" % content.DEFAULT_LANG):
            # The switcher's English link (/en/...): the static copy has no
            # language memory to reset, so it links the plain page.
            path = path[len(content.DEFAULT_LANG) + 1:] or "/"
        if path in self.pages or path == "/":
            return self.base + (path if path == "/" else path + "/") + suffix
        if path.startswith("/spk_website_v2/static/"):
            self.assets.add(path)
            return self.base + path + suffix
        if path.startswith("/web/assets/") and path.endswith(".css"):
            self.assets.add(path)
            return self.base + "/assets/site.css"
        if path == "/website/spk/enquiry":
            return self.base + "/contact/"
        # Routes another module serves (instruction site, portal entry, legacy noindex
        # page). That host may not have the same website languages: drop the prefix
        # and hand the instruction site its language as ?lang= instead.
        code, _sep, rest = path[1:].partition("/")
        if code in {lang for lang, _odoo, _name in content.SITE_LANGS} and rest:
            path = "/" + rest
            if path in content.INSTRUCTION_PATHS:
                suffix = "?lang=" + code + ("#" + parts.fragment if parts.fragment else "")
        return self.external + path + suffix

    def page(self, body):
        doc = lxml_html.document_fromstring(body)
        for script in doc.xpath("//script[@id='web.layout.odooscript']"):
            script.getparent().remove(script)
        for token in doc.xpath("//input[@name='csrf_token']"):
            token.set("value", "")
        for rules in doc.xpath("//script[@id='spk-setup-rules']"):
            # The setup guide builds its "Read next" links from this data.
            data = json.loads(rules.text)
            data["links"] = {key: [label, self.url(path)] for key, (label, path) in data["links"].items()}
            rules.text = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
        for element in doc.iter():
            if not isinstance(element.tag, str):
                continue
            for attribute in URL_ATTRIBUTES:
                if element.get(attribute):
                    element.set(attribute, self.url(element.get(attribute)))
            if element.get("srcset"):
                element.set("srcset", ", ".join(
                    " ".join([self.url(part.split()[0])] + part.split()[1:]) for part in element.get("srcset").split(",")))
        return lxml_html.tostring(doc, doctype="<!DOCTYPE html>", encoding="unicode", method="html")


def redirect_page(base, source, target):
    destination = base.rstrip("/") + target + ("/" if target != "/" else "")
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"robots\" content=\"noindex\">"
            "<link rel=\"canonical\" href=\"%s\">"
            "<meta http-equiv=\"refresh\" content=\"0; url=%s\">"
            "<title>Moved</title></head><body><p>%s has moved to <a href=\"%s\">%s</a>. "
            "The live site answers this address with a permanent (301) redirect.</p></body></html>\n"
            % (content.canonical_url(target), destination, source, destination, target))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--odoo", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--external", required=True)
    args = parser.parse_args()
    odoo = args.odoo.rstrip("/")

    status, probe = fetch(odoo + "/platform")
    if b"preview-banner" not in probe:
        raise SystemExit("Turn spk_website_v2.preview_mode on before exporting: a review copy must be noindex.")

    pages = page_paths(odoo)
    rewriter = Rewriter(args.base, pages, args.external)
    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    for path in pages:
        status, body = fetch(odoo + path)
        if status != 200:
            raise SystemExit("%s answered %s" % (path, status))
        target = args.out / path.strip("/") / "index.html" if path != "/" else args.out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rewriter.page(body), encoding="utf-8")

    status, body = fetch(odoo + "/this-page-does-not-exist")
    if status != 404:
        raise SystemExit("unknown URL answered %s, expected 404" % status)
    (args.out / "404.html").write_text(rewriter.page(body), encoding="utf-8")

    for source, (action, target) in content.LEGACY_ROUTES.items():
        if action == "redirect":
            folder = args.out / source.strip("/")
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "index.html").write_text(redirect_page(args.base, source, target), encoding="utf-8")
    folder = args.out / "products/smartphonekey-reader-1"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(
        redirect_page(args.base, "/products/smartphonekey-reader-1", "/products/readers"), encoding="utf-8")

    for asset in sorted(rewriter.assets):
        status, body = fetch(odoo + asset)
        if status != 200:
            raise SystemExit("asset %s answered %s" % (asset, status))
        destination = args.out / ("assets/site.css" if asset.startswith("/web/assets/") else asset.lstrip("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(body)

    (args.out / ".nojekyll").write_text("")
    (args.out / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    leftovers = [str(path) for path in args.out.rglob("*.html") if re.search(
        r"127\.0\.0\.1|localhost:8069|csrf_token: \"", path.read_text(encoding="utf-8"))]
    if leftovers:
        raise SystemExit("local addresses or tokens left in: %s" % leftovers)
    print("pages: %d, redirects: %d, assets: %d" % (
        len(pages), sum(1 for action, _t in content.LEGACY_ROUTES.values() if action == "redirect") + 1,
        len(rewriter.assets)))


if __name__ == "__main__":
    main()
