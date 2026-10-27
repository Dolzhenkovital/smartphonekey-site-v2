# -*- coding: utf-8 -*-
from lxml import html as lxml_html

from odoo.tests import HttpCase

from .. import site_content as content
from ..rendering import ENABLED_PARAM, PREVIEW_PARAM


class SiteCase(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        params = cls.env["ir.config_parameter"].sudo()
        params.set_param(ENABLED_PARAM, "True")
        params.set_param(PREVIEW_PARAM, "False")
        # The robots/sitemap tests need an indexable host: no fixed domain.
        cls.env["website"].search([]).write({"domain": False})

    def get(self, path, **kwargs):
        return self.url_open(path, allow_redirects=False, **kwargs)

    def page(self, path):
        response = self.get(path)
        self.assertEqual(response.status_code, 200, "%s answered %s" % (path, response.status_code))
        return response, lxml_html.fromstring(response.content)

    def all_page_paths(self):
        paths = [path for path in content.ROUTES if path != "/thank-you"]
        paths += ["/resources/%s" % slug for slug in (
            "lte-vs-wifi-access-control", "mifare-classic-desfire-ev3",
            "matter-thread-access-control", "access-control-when-offline")]
        return paths
