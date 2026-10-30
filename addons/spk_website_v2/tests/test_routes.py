# -*- coding: utf-8 -*-
from lxml import html as lxml_html

from odoo.tests import tagged

from .. import site_content as content
from ..rendering import ENABLED_PARAM
from .common import SiteCase


@tagged("post_install", "-at_install")
class TestRoutes(SiteCase):

    def test_required_routes_are_substantive_and_unique(self):
        titles, descriptions = {}, {}
        for path in self.all_page_paths():
            response, doc = self.page(path)
            self.assertEqual(len(doc.xpath("//h1")), 1, "%s needs exactly one h1" % path)
            title = doc.findtext(".//title")
            description = doc.xpath("//meta[@name='description']/@content")[0]
            self.assertNotIn(title, titles, "%s repeats the title of %s" % (path, titles.get(title)))
            self.assertNotIn(description, descriptions, "%s repeats a description" % path)
            titles[title], descriptions[description] = path, path
            canonical = doc.xpath("//link[@rel='canonical']/@href")
            self.assertEqual(canonical, [content.canonical_url(path)])
            main_text = " ".join(doc.xpath("//main")[0].text_content().split())
            self.assertGreater(len(main_text.split()), 60, "%s has too little text" % path)
            for placeholder in ("lorem", "TODO", "TBD", "placeholder"):
                self.assertNotIn(placeholder.lower(), main_text.lower(), "%s contains %s" % (path, placeholder))
            self.assertFalse(doc.xpath("//meta[@name='robots']"), "%s must be indexable" % path)
            self.assertNotIn("X-Robots-Tag", response.headers)

    def test_route_metadata_matches_register(self):
        for path, route in content.ROUTES.items():
            if path in ("/thank-you",):
                continue
            _response, doc = self.page(path)
            self.assertEqual(doc.findtext(".//title"), route["title"])

    def test_thank_you_is_noindex_and_claims_nothing_without_an_enquiry(self):
        response, doc = self.page("/thank-you")
        self.assertEqual(doc.xpath("//meta[@name='robots']/@content"), ["noindex, nofollow"])
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex, nofollow")
        self.assertNotIn("has been received", doc.xpath("//h1")[0].text_content())

    def test_content_is_server_rendered(self):
        """A03: the answers are in the HTML, not built by a script."""
        expectations = {
            "/": ["Your key to access control.", "Manage access across your properties in one place",
                  "Get help in the Admin Panel with the built-in AI Assistant.",
                  "Changes for an offline reader remain pending until it reconnects and applies them."],
            "/platform": ["SmartphoneKey is an access management platform."],
            "/products/readers": ["LTE reader", "Wi-Fi reader", "A SIM and cellular service for each reader"],
            "/resources/lte-vs-wifi-access-control": ["LTE reader", "Choose the connection that fits the site"],
            "/compatibility": ["MIFARE Classic", "MIFARE DESFire EV3"],
            "/find-your-setup": [content.SETUP_CONNECTION_ADVICE["wifi"]],
            "/contact": ["Send enquiry", "info@smartphonekey.com"],
        }
        for path, phrases in expectations.items():
            _response, doc = self.page(path)
            text = " ".join(doc.text_content().split())
            for phrase in phrases:
                self.assertIn(phrase, text, "%s is missing %r" % (path, phrase))
            self.assertTrue(doc.xpath("//nav[@aria-label='Main']//a[@href='/platform']"))

    def test_product_screenshots_are_served_and_described(self):
        """The real Admin Panel captures of 30 October 2026: every product image a page shows exists,
        has alt text, and its expanded view points at an existing full-size file."""
        # Home: Dashboard, Assign Key, Guest Key, Recent activity, AI Assistant (the phone close-up is a <source>).
        pages = {"/": 5, "/platform": 2, "/platform/access-management": 4, "/products/readers": 0}
        for path, minimum in pages.items():
            _response, doc = self.page(path)
            images = doc.xpath("//main//img[contains(@src, '/img/product-ui/')]")
            self.assertGreaterEqual(len(images), minimum, "%s shows too few product screenshots" % path)
            for image in images + doc.xpath("//main//source[contains(@srcset, '/img/product-ui/')]"):
                for src in (image.get("src") or image.get("srcset")).split(","):
                    self.assertEqual(self.get(src.split()[0]).status_code, 200, src)
                if image.tag == "img":
                    self.assertTrue(image.get("alt"), image.get("src"))
                    self.assertTrue(image.get("width") and image.get("height"), image.get("src"))
            for link in doc.xpath("//main//a[@data-spk-expand]"):
                self.assertEqual(self.get(link.get("href")).status_code, 200, link.get("href"))
                self.assertTrue(link.get("data-spk-expand-alt"))
        # The home page's largest image is the eager one; every other product image is lazy.
        _response, doc = self.page("/")
        eager = doc.xpath("//main//img[@fetchpriority='high']")
        self.assertEqual(len(eager), 1)
        self.assertIn("admin-dashboard", eager[0].get("src"))
        for image in doc.xpath("//main//img[contains(@src, '/img/product-ui/')][not(@fetchpriority)]"):
            self.assertEqual(image.get("loading"), "lazy", image.get("src"))

    def test_setup_result_without_javascript(self):
        _response, doc = self.page("/find-your-setup?role=integrator&sites=eleven_plus&connection=cellular"
                                   "&interests=cards&interests=bogus&email=someone@example.com")
        text = " ".join(doc.text_content().split())
        self.assertIn(content.SETUP_CONNECTION_ADVICE["cellular"], text)
        self.assertIn("MIFARE Classic and MIFARE DESFire EV3", text)
        contact = doc.xpath("//a[@data-spk-result-contact]/@href")[0]
        self.assertEqual(contact, "/contact?interest=project&role=integrator&sites=eleven_plus"
                                  "&connection=cellular&interests=cards")
        self.assertNotIn("example.com", contact)
        # The home hero's compact tool hands over its two choices.
        _response, doc = self.page("/find-your-setup?site=partner&connection=wifi")
        self.assertIn("Plan the installation, the handover to the customer's site administrators", " ".join(doc.text_content().split()))

    def test_certifications_and_instructions_are_reachable(self):
        """Every page links the certificates and the instructions from its navigation."""
        _response, doc = self.page("/")
        self.assertTrue(doc.xpath("//nav[@aria-label='Main']//a[@href='/certifications']"))
        self.assertTrue(doc.xpath("//nav[@aria-label='Main']//a[@href='/guide-for-usage-and-installation']"))
        # The existing instruction page, linked from the header of every page.
        self.assertTrue(doc.xpath("//div[@class='header-actions']/a[@href='/guide-for-usage-and-installation']"))
        for path in content.INSTRUCTION_PATHS:
            self.assertTrue(doc.xpath("//footer//a[@href='%s']" % path), path)
        _response, doc = self.page("/resources")
        section = doc.xpath("//section[@id='instructions']")[0]
        for path in list(content.INSTRUCTION_PATHS) + ["/certifications", "/apps-and-chatbot"]:
            self.assertTrue(section.xpath(".//a[@href='%s']" % path), path)
        _response, doc = self.page("/certifications")
        self.assertEqual(len(doc.xpath("//table")), 2)
        self.assertTrue(doc.xpath("//a[contains(@href, '/spk_website_v2/static/src/files/')]"))

    def test_contact_prefill_takes_enums_only(self):
        _response, doc = self.page("/contact?interest=visitor&role=owner&sites=nonsense&name=Mallory")
        self.assertEqual(doc.xpath("//select[@name='enquiry_type']/option[@selected]/@value"), ["project"])
        self.assertEqual(doc.xpath("//select[@name='role']/option[@selected]/@value"), ["owner"])
        self.assertFalse(doc.xpath("//select[@name='sites']/option[@selected]"))
        self.assertEqual(doc.xpath("//input[@name='interests'][@checked]/@value"), ["visitors"])
        self.assertEqual(doc.xpath("//input[@name='name']/@value"), [])

    def test_unknown_route_is_a_real_404(self):
        response = self.get("/no-such-page")
        self.assertEqual(response.status_code, 404)
        doc = lxml_html.fromstring(response.content)
        self.assertEqual(doc.xpath("//h1")[0].text_content(), "This page is not here.")
        self.assertEqual(self.get("/resources/no-such-guide").status_code, 404)
        self.assertEqual(self.get("/post/no-such-post").status_code, 404)
        self.assertEqual(self.get("/team/no-such-person").status_code, 404)

    def test_marketing_assets_stay_off_the_login_page(self):
        """A15: the 2.0 bundle and its class never reach Odoo's own pages."""
        response = self.get("/web/login")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"spk_website_v2", response.content)
        self.assertNotIn(b"spk-site-v2", response.content)

    def test_switch_hands_the_site_back_to_the_baseline(self):
        params = self.env["ir.config_parameter"].sudo()
        params.set_param(ENABLED_PARAM, "False")
        self.assertEqual(self.get("/platform").status_code, 404)
        self.assertEqual(self.get("/features").status_code, 200)
        self.assertIn(b"data-wf-site", self.get("/").content)
        params.set_param(ENABLED_PARAM, "True")
        self.assertEqual(self.get("/features").status_code, 301)
