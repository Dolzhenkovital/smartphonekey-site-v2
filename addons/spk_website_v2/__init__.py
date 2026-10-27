from . import controllers
from . import models
from .site_content import SITE_LANGS


def post_init_hook(env):
    """Activate the site's languages and offer them on every website.

    Odoo then serves /fr/, /de/, /es/ and /uk/ copies of each page. The terms
    of every installed module are loaded for languages that were not active
    before, so the rest of the website does not appear half translated."""
    Lang = env["res.lang"]
    added = []
    langs = Lang.browse()
    for _url_code, code, _name in SITE_LANGS:
        lang = Lang.with_context(active_test=False).search([("code", "=", code)])
        if not lang.active:
            added.append(code)
        langs |= Lang._activate_lang(code)
    for website in env["website"].search([]):
        website.language_ids |= langs
    if added:
        modules = env["ir.module.module"].search([("state", "in", ("installed", "to install", "to upgrade"))])
        env["ir.module.module"]._load_module_terms(sorted(set(modules.mapped("name")) | {"spk_website_v2"}), added)
