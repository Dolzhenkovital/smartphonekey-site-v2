# -*- coding: utf-8 -*-
"""Short-lived throttle records for the public enquiry form.

A visitor is identified by a keyed hash of their address that changes every
day; the full address is never stored, and records older than a day are
removed by the autovacuum.
"""

import hashlib
import hmac
from datetime import timedelta

from odoo import api, fields, models

WINDOW_MINUTES = 10
MAX_ATTEMPTS = 5


class SpkWebsiteEnquiryAttempt(models.Model):
    _name = "spk.website.enquiry.attempt"
    _description = "SmartphoneKey website enquiry attempt"
    _order = "id desc"

    client_key = fields.Char(required=True, index=True)

    @api.model
    def _spk_client_key(self, remote_addr):
        secret = self.env["ir.config_parameter"].sudo().get_param("database.secret") or ""
        day = fields.Date.context_today(self).isoformat()
        message = ("%s|%s" % (day, remote_addr or "")).encode()
        return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()[:32]

    @api.model
    def _spk_register_attempt(self, remote_addr):
        """Record one attempt; False when the visitor is over the limit."""
        key = self._spk_client_key(remote_addr)
        since = fields.Datetime.now() - timedelta(minutes=WINDOW_MINUTES)
        Attempt = self.sudo()
        if Attempt.search_count([("client_key", "=", key), ("create_date", ">=", since)]) >= MAX_ATTEMPTS:
            return False
        Attempt.create({"client_key": key})
        return True

    @api.autovacuum
    def _gc_spk_attempts(self):
        self.sudo().search([("create_date", "<", fields.Datetime.now() - timedelta(days=1))]).unlink()
