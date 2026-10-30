# -*- coding: utf-8 -*-
import json
import re
from urllib import robotparser

from lxml import etree, html as lxml_html

from odoo.tests import tagged

from .. import site_content as content
from ..rendering import PREVIEW_PARAM
from .common import SiteCase

SEARCH_BOTS = ("Googlebot", "Bingbot", "OAI-SearchBot", "Claude-SearchBot")
TRAINING_BOTS = ("GPTBot", "ClaudeBot")
# A05-A08: wording the claim register does not allow on the 2.0 pages.
FORBIDDEN = (
    (re.compile(r"\b80\s?(m|metres|meters)\b", re.I), "a link distance"),
    (re.compile(r"\bEV1\b|\bEV2\b"), "a DESFire generation other than EV3"),
    (re.compile(r"\b(1K|4K|2K|8K)\b"), "a card memory size"),
    (re.compile(r"any matter device|all matter devices|every matter device works", re.I), "universal Matter support"),
    (re.compile(r"unlimited|any complexity", re.I), "unlimited scenarios"),
    (re.compile(r"generally available|available now", re.I), "Concierge availability"),
    (re.compile(r"bank-grade|unhackable|uncopyable|non-copyable|fully compliant", re.I), "an umbrella security claim"),
    (re.compile(r"(?<!no )automatic failover(?! is not)", re.I), "failover"),
    (re.compile(r"\$\s?\d|€\s?\d|£\s?\d|\bprice\b", re.I), "a price"),
    (re.compile(r"book a demo|request a demo", re.I), "a demo funnel"),
    # Brief of 30 October 2026: no instant revocation, no unconditional assistant promise, no unmeasured savings.
    (re.compile(r"revoke[sd]? (access |their access )?instantly|instant revocation", re.I), "instant revocation"),
    (re.compile(r"handles the rest|just ask\.", re.I), "an unconditional assistant promise"),
    (re.compile(r"access in seconds|less training|faster management", re.I), "an unmeasured saving"),
)


@tagged("post_install", "-at_install")
class TestDiscovery(SiteCase):

    def test_sitemap_lists_published_canonical_pages_only(self):
        response = self.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        tree = etree.fromstring(response.content)
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [loc.split("/", 3)[-1] for loc in tree.xpath("//s:loc/text()", namespaces=namespace)]
        paths = {"/" + loc if not loc.startswith("/") else loc for loc in locs}
        for path in self.all_page_paths():
            self.assertIn(path, paths)
        for absent in ("/thank-you", "/features", "/blog", "/referral-program", "/404", "/adminpanel"):
            self.assertNotIn(absent, paths)
        for path in paths:
            if path.startswith(("/guide-for", "/instructions/")):
                continue
            # A fresh visitor each time: Odoo remembers the last language in a cookie.
            self.opener.cookies.clear()
            self.assertEqual(self.get(path).status_code, 200, path)

    def test_robots_keeps_search_and_training_decisions_separate(self):
        text = self.get("/robots.txt").content.decode()
        parser = robotparser.RobotFileParser()
        parser.parse(text.splitlines())
        for agent in SEARCH_BOTS + TRAINING_BOTS:
            self.assertTrue(parser.can_fetch(agent, "/platform"), agent)
            self.assertTrue(parser.can_fetch(agent, "/resources/matter-thread-access-control"), agent)
            for private in ("/my", "/my/spk-portal", "/odoo", "/web/login", "/website/spk/enquiry"):
                self.assertFalse(parser.can_fetch(agent, private), "%s may fetch %s" % (agent, private))
        self.assertIn("Sitemap:", text)

    def test_preview_is_never_indexed(self):
        params = self.env["ir.config_parameter"].sudo()
        params.set_param(PREVIEW_PARAM, "True")
        try:
            parser = robotparser.RobotFileParser()
            parser.parse(self.get("/robots.txt").content.decode().splitlines())
            self.assertFalse(parser.can_fetch("Googlebot", "/platform"))
            response, doc = self.page("/platform")
            self.assertEqual(doc.xpath("//meta[@name='robots']/@content"), ["noindex, nofollow"])
            self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex, nofollow")
            self.assertTrue(doc.xpath("//p[@class='preview-banner']"))
        finally:
            params.set_param(PREVIEW_PARAM, "False")
        _response, doc = self.page("/platform")
        self.assertFalse(doc.xpath("//meta[@name='robots']"))

    def test_structured_data_matches_the_page(self):
        """A18: parseable, one block, visible facts only, nothing invented."""
        for path in self.all_page_paths() + ["/post/%s" % content.LEGACY_POSTS[0]]:
            _response, doc = self.page(path)
            blocks = doc.xpath("//script[@type='application/ld+json']/text()")
            self.assertEqual(len(blocks), 1, path)
            data = json.loads(blocks[0])
            all_types, all_keys = set(), set()

            def walk(node):
                if isinstance(node, dict):
                    all_keys.update(node)
                    if "@type" in node:
                        all_types.add(node["@type"])
                    for value in node.values():
                        walk(value)
                elif isinstance(node, list):
                    for value in node:
                        walk(value)
            walk(data)
            invented_types = {"Offer", "AggregateRating", "Review", "PostalAddress", "SearchAction", "FAQPage", "Product"}
            invented_keys = {"offers", "aggregateRating", "review", "price", "gtin", "sku", "mpn", "address"}
            self.assertFalse(all_types & invented_types, "%s declares %s" % (path, all_types & invented_types))
            self.assertFalse(all_keys & invented_keys, "%s declares %s" % (path, all_keys & invented_keys))
            types = {node["@type"] for node in data["@graph"]}
            page = next(node for node in data["@graph"] if node["@id"].endswith("#webpage"))
            self.assertEqual(page["url"], content.canonical_url(path))
            if path == "/":
                self.assertTrue({"Organization", "WebSite"} <= types)
            else:
                crumbs = next(node for node in data["@graph"] if node["@type"] == "BreadcrumbList")
                visible = [" ".join(item.text_content().split())
                           for item in doc.xpath("//nav[@aria-label='Breadcrumb']//li")]
                self.assertEqual([item["name"] for item in crumbs["itemListElement"]], visible, path)
            if path.startswith(("/resources/", "/post/")):
                article = next(node for node in data["@graph"] if node["@type"] == "Article")
                self.assertEqual(article["headline"], doc.xpath("//h1")[0].text_content())
                self.assertRegex(article["datePublished"], r"^\d{4}-\d{2}-\d{2}$")

    def test_claim_scope_on_the_new_pages(self):
        for path in self.all_page_paths() + ["/certifications", "/apps-and-chatbot"]:
            _response, doc = self.page(path)
            for script in doc.xpath("//script"):
                script.drop_tree()
            text = " ".join(doc.text_content().split())
            for pattern, what in FORBIDDEN:
                match = pattern.search(text)
                self.assertFalse(match, "%s states %s: %r" % (path, what, match and match.group(0)))
        # Accepted is not opened; pending is not enforced.
        _response, doc = self.page("/resources/access-control-when-offline")
        text = " ".join(doc.text_content().split())
        self.assertIn("It does not prove a person passed through or the door opened.", text)
        self.assertIn("A revocation made while a reader is offline is pending, not enforced.", text)
        _response, doc = self.page("/platform/visitor-access")
        self.assertIn("Confirm availability and the required setup with our team.", doc.text_content())
        # Owner instruction of 2026-10-27: every reader is a Thread router and Border Router.
        _response, doc = self.page("/products/readers")
        text = " ".join(doc.text_content().split())
        self.assertIn("Each SmartphoneKey reader can act as a Thread Border Router and as a router in the Thread mesh.", text)
        self.assertNotIn("Do not assume every reader is a Border Router", text)

    def test_open_graph(self):
        for path in ("/", "/platform", "/products/readers"):
            _response, doc = self.page(path)
            image = doc.xpath("//meta[@property='og:image']/@content")[0]
            self.assertTrue(image.startswith(content.ORIGIN + "/spk_website_v2/static/src/img/"))
            self.assertEqual(self.get(image[len(content.ORIGIN):]).status_code, 200)
            self.assertTrue(doc.xpath("//meta[@property='og:image:alt']/@content")[0])
