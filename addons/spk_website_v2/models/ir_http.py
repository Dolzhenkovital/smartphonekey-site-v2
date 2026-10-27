# -*- coding: utf-8 -*-
"""Unknown public URLs answer a real 404 in the 2.0 shell.

Only for visitors (code 404; a website designer gets Odoo's own "create this
page" 404) and only in the marketing site's space: the portal, the backend,
the instruction site and Odoo's technical routes keep Odoo's error pages.
"""

from odoo import models
from odoo.http import request

from ..rendering import is_v2_enabled

OWN_ERROR_PAGES = ("/my", "/web", "/odoo", "/website/", "/instructions/", "/guide-for-usage-and-installation")


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _get_error_html(cls, env, code, values):
        if code == 404 and request and is_v2_enabled(env) \
                and not request.httprequest.path.startswith(OWN_ERROR_PAGES):
            from ..controllers.main import render_not_found
            response = render_not_found()
            return 404, response.render()
        return super()._get_error_html(env, code, values)
