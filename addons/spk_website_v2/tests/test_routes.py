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
            "/": ["Your key to access control.", "Start with Wi-Fi coverage at each reader location."],
            "/platform": ["SmartphoneKey is an access control management platform."],
            "/products/readers": ["LTE reader", "Wi-Fi reader", "Cellular coverage and suitable SIM and service"],
            "/resources/lte-vs-wifi-access-control": ["LTE reader", "Choose the connection that fits the site"],
            "/compatibility": ["MIFARE Classic", "MIFARE DESFire EV3"],
            "/find-your-setup": ["Start by checking Wi-Fi coverage and network requirements"],
            "/contact": ["Send enquiry", "info@smartphonekey.com"],
        }
        for path, phrases in expectations.items():
            _response, doc = self.page(path)
            text = " ".join(doc.text_content().split())
            for phrase in phrases:
                self.assertIn(phrase, text, "%s is missing %r" % (path, phrase))
            self.assertTrue(doc.xpath("//nav[@aria-label='Main']//a[@href='/platform']"))

    def test_setup_result_without_javascript(self):
        _response, doc = self.page("/find-your-setup?role=integrator&sites=eleven_plus&connection=cellular"
                                   "&interests=cards&interests=bogus&email=someone@example.com")
        text = " ".join(doc.text_content().split())
        self.assertIn("Discuss LTE coverage, SIM provisioning and the reader model for your installation.", text)
        self.assertIn("MIFARE Classic and MIFARE DESFire EV3", text)
        contact = doc.xpath("//a[@data-spk-result-contact]/@href")[0]
        self.assertEqual(contact, "/contact?interest=project&role=integrator&sites=eleven_plus"
                                  "&connection=cellular&interests=cards")
        self.assertNotIn("example.com", contact)
        # The home hero's compact tool hands over its two choices.
        _response, doc = self.page("/find-your-setup?site=partner&connection=wifi")
        self.assertIn("Plan the installation, the customer handover", doc.text_content())

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
