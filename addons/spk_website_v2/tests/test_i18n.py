# -*- coding: utf-8 -*-
import json
import re
from os.path import join

import polib
from lxml import etree, html as lxml_html

from odoo.modules.module import get_module_path
from odoo.tests import tagged
from odoo.tools.translate import code_translations

from .. import site_content as content
from .common import SiteCase

TRANSLATED = [(code, odoo) for code, odoo, _name in content.SITE_LANGS if code != content.DEFAULT_LANG]


def catalogue(code):
    po = polib.pofile(join(get_module_path("spk_website_v2"), "i18n", "%s.po" % code))
    return {entry.msgid: entry.msgstr for entry in po}


@tagged("post_install", "-at_install")
class TestLanguages(SiteCase):

    def test_every_site_string_is_translated(self):
        """Like the portal's i18n gate: each language covers every string the code shows."""
        for code, odoo in TRANSLATED:
            translations = code_translations.get_python_translations("spk_website_v2", odoo)
            missing = [text for text in content.translatable_strings() if not translations.get(text)]
            self.assertFalse(missing, "%s lacks %d strings, e.g. %s" % (code, len(missing), missing[:3]))
            for text, translation in catalogue(code).items():
                if translation:
                    self.assertEqual(sorted(re.findall(r"%\([a-z_]+\)s", text)),
                                     sorted(re.findall(r"%\([a-z_]+\)s", translation)),
                                     "%s: placeholders of %r" % (code, text))

    def test_pages_render_in_each_language(self):
        english_h1 = "How SmartphoneKey works"
        for code, _odoo in TRANSLATED:
            response, doc = self.page("/%s/platform" % code)
            self.assertEqual(doc.get("lang"), code)
            self.assertEqual(response.headers.get("Content-Language"), code)
            h1 = doc.xpath("//h1")[0].text_content()
            self.assertEqual(h1, catalogue(code)[english_h1])
            self.assertNotEqual(h1, english_h1)
            self.assertEqual(doc.xpath("//link[@rel='canonical']/@href"), [content.ORIGIN + "/%s/platform" % code])
            alternates = dict(zip(doc.xpath("//link[@rel='alternate']/@hreflang"), doc.xpath("//link[@rel='alternate']/@href")))
            self.assertEqual(set(alternates), {lang for lang, _o, _n in content.SITE_LANGS} | {"x-default"})
            self.assertEqual(alternates["x-default"], content.ORIGIN + "/platform")
            # Site links carry the language; the switcher keeps every language.
            self.assertTrue(doc.xpath("//nav[@class='desktop-nav']//a[@href='/%s/compatibility']" % code))
            for other, _o, _n in content.SITE_LANGS:
                self.assertTrue(doc.xpath("//header//a[@hreflang='%s']" % other), "%s switcher lacks %s" % (code, other))
            data = json.loads(doc.xpath("//script[@type='application/ld+json']/text()")[0])
            page = next(node for node in data["@graph"] if node["@id"].endswith("#webpage"))
            self.assertEqual(page["inLanguage"], code)

    def test_english_only_pages(self):
        for path in ("/fr/privacy-policy", "/de/post/%s" % content.LEGACY_POSTS[0], "/uk/team/vadym-sydorenko"):
            _response, doc = self.page(path)
            english_path = "/" + path.split("/", 2)[2]
            self.assertEqual(doc.xpath("//link[@rel='canonical']/@href"), [content.ORIGIN + english_path])
            self.assertFalse(doc.xpath("//link[@rel='alternate']"))
            self.assertTrue(doc.xpath("//p[contains(@class, 'english-only')]"), path)

    def test_sitemap_lists_each_language_copy(self):
        body = self.get("/sitemap.xml").content
        locs = etree.fromstring(body).xpath("//s:loc/text()", namespaces={"s": "http://www.sitemaps.org/schemas/sitemap/0.9"})
        paths = {loc.split("/", 3)[-1] for loc in locs}
        for code, _odoo in TRANSLATED:
            self.assertIn("%s/platform" % code, paths)
            self.assertIn("%s/resources/matter-thread-access-control" % code, paths)
            self.assertNotIn("%s/privacy-policy" % code, paths)
            self.assertNotIn("%s/post/%s" % (code, content.LEGACY_POSTS[0]), paths)

    def test_setup_guide_and_enquiry_speak_the_visitor_language(self):
        terms = catalogue("uk")
        _response, doc = self.page("/uk/find-your-setup?connection=cellular&interests=cards")
        text = " ".join(doc.text_content().split())
        self.assertIn(terms[content.SETUP_CONNECTION_ADVICE["cellular"]], text)
        contact = doc.xpath("//a[@data-spk-result-contact]/@href")[0]
        self.assertTrue(contact.startswith("/uk/contact?"), contact)
        rules = json.loads(doc.xpath("//script[@id='spk-setup-rules']/text()")[0])
        self.assertEqual(rules["links"]["cards"][1], "/uk/resources/mifare-classic-desfire-ev3")

        _response, doc = self.page("/de/contact")
        token = doc.xpath("//input[@name='csrf_token']/@value")[0]
        submission = doc.xpath("//input[@name='submission_id']/@value")[0]
        self.assertTrue(doc.xpath("//form[@action='/de/website/spk/enquiry']"))
        response = self.url_open("/de/website/spk/enquiry", data={
            "csrf_token": token, "submission_id": submission, "name": "T", "email": "x",
            "enquiry_type": "project"}, headers={"Accept": "application/json"}, allow_redirects=False)
        fields = response.json()["fields"]
        self.assertEqual(fields["name"], catalogue("de")["Enter your name, between 2 and 120 characters."])

        response = self.url_open("/de/website/spk/enquiry", data={
            "csrf_token": token, "submission_id": submission, "name": "Test Besucher",
            "email": "test.besucher@example.com", "enquiry_type": "partner"},
            headers={"Accept": "application/json"}, allow_redirects=False)
        self.assertTrue(response.json()["ok"])
        lead = self.env["crm.lead"].sudo().search([("spk_submission_id", "=", submission)])
        self.assertEqual(lead.lang_id.code, "de_DE")

    def test_dates_follow_the_language(self):
        _response, doc = self.page("/fr/compatibility")
        self.assertIn("octobre 2026", doc.xpath("//p[@class='meta']")[0].text_content())
