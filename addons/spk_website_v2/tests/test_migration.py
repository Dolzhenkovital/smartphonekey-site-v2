# -*- coding: utf-8 -*-
from urllib.parse import urlsplit

from odoo.tests import tagged

from .. import site_content as content
from .common import SiteCase


@tagged("post_install", "-at_install")
class TestMigration(SiteCase):
    """A16/A17: every URL of the Webflow snapshot answers as decided."""

    def test_every_snapshot_url_has_its_intended_answer(self):
        instruction_site = self.env["ir.module.module"].sudo().search_count(
            [("name", "=", "smartphonekey"), ("state", "=", "installed")])
        for source, (action, target) in content.LEGACY_ROUTES.items():
            response = self.get(source)
            if action == "redirect":
                self.assertEqual(response.status_code, 301, source)
                location = urlsplit(response.headers["Location"]).path
                self.assertEqual(location, target, source)
                final = self.get(target)
                self.assertEqual(final.status_code, 200, "%s -> %s must end on a page, not a chain" % (source, target))
            elif action == "retain":
                self.assertEqual(response.status_code, 200, source)
                self.assertIn(b"spk-site-v2", response.content, "%s should be in the 2.0 shell" % source)
            elif action == "not_found":
                self.assertEqual(response.status_code, 404, source)
            elif action == "instruction_site":
                if instruction_site:
                    self.assertEqual(response.status_code, 200, source)
            elif action == "baseline":
                # Served by the AP-428 module exactly as before.
                self.assertIn(response.status_code, (200, 302, 303), source)
                self.assertNotIn(b"spk-site-v2", response.content, source)

    def test_kept_articles_and_team_pages(self):
        for slug in content.LEGACY_POSTS:
            response, doc = self.page("/post/%s" % slug)
            self.assertTrue(doc.xpath("//p[@class='archive-note']"), slug)
            self.assertFalse(doc.xpath("//a[contains(@href, 'smartphonekey-reader-1')]"), slug)
            self.assertFalse(doc.xpath("//iframe"), slug)
        for slug in content.LEGACY_TEAM:
            self.page("/team/%s" % slug)

    def test_referral_page_is_neither_linked_nor_in_the_sitemap(self):
        for path in self.all_page_paths():
            self.assertNotIn(b'href="/referral-program"', self.get(path).content, path)
        self.assertNotIn(b"/referral-program", self.get("/sitemap.xml").content)

    def test_no_new_page_links_to_the_old_webflow_urls(self):
        old = [source for source, (action, _target) in content.LEGACY_ROUTES.items() if action == "redirect"]
        for path in self.all_page_paths():
            body = self.get(path).content
            for source in old:
                self.assertNotIn(('href="%s"' % source).encode(), body, "%s links to %s" % (path, source))
