# -*- coding: utf-8 -*-
"""18.0.3.0.0: bring the revised content records into existing databases.

The claim register, the compatibility rows and the four guides are ``noupdate``
records: a normal module update leaves them as the editors last saw them, so a
database installed before this release would keep the old card-programming
wording (claim C05 was clarified on 27 October 2026), the old compatibility rows
and the old guide bodies. This script loads the three data files again with
``noupdate`` ignored (mode "init" is what makes Odoo write records whose XML id is
flagged noupdate), then makes sure the two card-programming rows are published
with the verification date of the clarification.

It overwrites every editor change made to those records since installation.
Translations of the rewritten fields are loaded from i18n/*.po by a module update
with ``--i18n-overwrite``.
"""
import logging
from datetime import date

from odoo import SUPERUSER_ID, api
from odoo.tools import convert

_logger = logging.getLogger(__name__)

MODULE = "spk_website_v2"
DATA_FILES = ("data/website_claims.xml", "data/website_compatibility.xml", "data/website_resources.xml")
CARD_ROWS = ("compat_mifare_classic", "compat_mifare_desfire_ev3")
CLARIFIED_ON = date(2026, 10, 27)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for path in DATA_FILES:
        convert.convert_file(env, MODULE, path, {}, mode="init", noupdate=False, kind="data")
        _logger.info("%s 18.0.3.0.0: reloaded %s (editor changes to its records were overwritten)", MODULE, path)
    for name in CARD_ROWS:
        row = env.ref("%s.%s" % (MODULE, name), raise_if_not_found=False)
        if not row:
            _logger.warning("%s 18.0.3.0.0: compatibility row %s not found", MODULE, name)
            continue
        # The model sends an edited published row back to review; publish it again, as the XML says.
        row.sudo().write({"state": "published", "verified_at": CLARIFIED_ON})
        _logger.info("%s 18.0.3.0.0: %s is %s, verified %s", MODULE, name, row.state, row.verified_at)
