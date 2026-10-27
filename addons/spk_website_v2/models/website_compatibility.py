# -*- coding: utf-8 -*-
"""Curated compatibility rows for /compatibility and the reader pages.

A row is public only while it is published *and* its claim's publication
state allows public rows. Changing a technical field of a published row sends
it back to review: the edit stays off the site until a publisher approves it,
which also records the new verification date the page shows.
"""

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError

CATEGORIES = [
    ("cards", "Physical card programming"),
    ("digital", "Digital credentials"),
    ("matter", "Matter devices"),
    ("network", "Networks"),
    ("cameras", "Cameras"),
]
OPERATIONS = [
    ("read", "Read"),
    ("program", "Program"),
    ("control", "Control"),
    ("connect", "Connect"),
    ("manage", "Manage"),
]
STATES = [
    ("draft", "Draft"),
    ("review", "In review"),
    ("published", "Published"),
    ("withdrawn", "Withdrawn"),
]
# Fields whose change alters what the site claims.
TECHNICAL_FIELDS = frozenset({
    "category", "name", "revision", "firmware_scope", "operation", "capabilities",
    "limitations", "claim_id", "public_source_url",
})
# What the public pages may read of a row.
PUBLIC_FIELDS = ("category", "name", "revision", "firmware_scope", "operation", "capabilities",
                 "limitations", "verified_at", "public_source_url")


class SpkWebsiteCompatibility(models.Model):
    _name = "spk.website.compatibility"
    _description = "SmartphoneKey website compatibility row"
    _order = "category, sequence, id"

    sequence = fields.Integer(default=10)
    category = fields.Selection(CATEGORIES, required=True)
    name = fields.Char("Family or model", required=True, translate=True)
    revision = fields.Char()
    firmware_scope = fields.Char()
    operation = fields.Selection(OPERATIONS, required=True)
    capabilities = fields.Text("What it covers", required=True, translate=True)
    limitations = fields.Text("Conditions and limits", required=True, translate=True)
    verified_at = fields.Date("Verified on", readonly=True)
    evidence_ref = fields.Char(
        "Evidence reference", groups="spk_website_v2.group_spk_website_editor",
        help="Internal reference. Never rendered on the public site.")
    public_source_url = fields.Char("Public source")
    claim_id = fields.Many2one("spk.website.claim", required=True, ondelete="restrict")
    state = fields.Selection(STATES, required=True, default="draft", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su and not self.env.user.has_group("spk_website_v2.group_spk_website_publisher"):
            for vals in vals_list:
                if vals.get("state", "draft") not in ("draft", "review"):
                    raise AccessError(self.env._("Only a website publisher can publish a compatibility row."))
        return super().create(vals_list)

    def write(self, vals):
        if "state" in vals and not self.env.su \
                and not self.env.user.has_group("spk_website_v2.group_spk_website_publisher") \
                and vals["state"] not in ("draft", "review"):
            raise AccessError(self.env._("Only a website publisher can publish or withdraw a compatibility row."))
        if TECHNICAL_FIELDS.intersection(vals) and "state" not in vals:
            changed = self.filtered(lambda row: row.state == "published")
            if changed:
                super(SpkWebsiteCompatibility, changed).write(dict(vals, state="review"))
                return super(SpkWebsiteCompatibility, self - changed).write(vals)
        return super().write(vals)

    def action_submit_review(self):
        self.write({"state": "review"})

    def action_publish(self):
        if not self.env.user.has_group("spk_website_v2.group_spk_website_publisher"):
            raise AccessError(self.env._("Only a website publisher can publish a compatibility row."))
        for row in self:
            if not row.claim_id.allows_public_rows():
                raise UserError(self.env._(
                    "Claim %(claim)s is not cleared for public rows (%(state)s). Update the claim first.",
                    claim=row.claim_id.code, state=row.claim_id.publication))
        self.write({"state": "published", "verified_at": fields.Date.context_today(self)})

    def action_withdraw(self):
        self.write({"state": "withdrawn"})

    @api.model
    def _public_rows(self, category=None):
        """The published rows as plain dicts of public fields only."""
        domain = [("state", "=", "published")]
        if category:
            domain.append(("category", "=", category))
        rows = self.sudo().search(domain)
        rows = rows.filtered(lambda row: row.claim_id.allows_public_rows())
        operations = dict(OPERATIONS)
        result = []
        for row in rows:
            values = {field: row[field] or False for field in PUBLIC_FIELDS}
            values["operation_label"] = operations.get(row.operation, "")
            result.append(values)
        return result

    @api.model
    def _public_reviewed_on(self):
        """The latest verification date among the public rows, or False."""
        dates = [row["verified_at"] for row in self._public_rows() if row["verified_at"]]
        return max(dates) if dates else False
