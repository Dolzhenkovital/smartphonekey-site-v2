# -*- coding: utf-8 -*-
"""The claim register behind the site's technical copy.

Every capability statement the site makes traces to one claim: its stable
code, how strong the evidence is, how it may be published, the allowed
wording and its limitations. The register is internal; the public pages only
ever see what a claim's publication state lets through (see
``spk.website.compatibility._public_rows``), never its sources.
"""

from odoo import api, fields, models
from odoo.exceptions import UserError

EVIDENCE_LEVELS = [
    ("documented", "Documented"),
    ("code_supported", "Code-supported"),
    ("owner_stated", "Owner-stated"),
    ("release_gated", "Release-gated"),
    ("unverified", "Unverified"),
]
PUBLICATION_STATES = [
    ("draft", "Draft"),
    ("public_scoped", "Public, scoped"),
    ("fallback_only", "Fallback wording only"),
    ("omit_numeric", "Omit the number"),
    ("availability_enquiry", "Availability enquiry only"),
    ("document_links_only", "Document links only"),
    ("approved", "Approved"),
    ("withdrawn", "Withdrawn"),
]
# The states that let a compatibility row backed by the claim appear publicly.
PUBLIC_STATES = ("public_scoped", "approved")
OWNER_ROLES = [
    ("product_engineering", "Product engineering"),
    ("hardware_firmware", "Hardware and firmware"),
    ("product_owner", "Product owner"),
    ("marketing", "Marketing"),
    ("operations", "Operations"),
]


class SpkWebsiteClaim(models.Model):
    _name = "spk.website.claim"
    _description = "SmartphoneKey website claim"
    _order = "code"
    _rec_name = "display_label"

    code = fields.Char(required=True, help="Stable identifier (C01, C02, ...). It never changes once created.")
    name = fields.Char("Capability", required=True)
    display_label = fields.Char(compute="_compute_display_label")
    evidence_level = fields.Selection(EVIDENCE_LEVELS, required=True, default="unverified")
    publication = fields.Selection(PUBLICATION_STATES, required=True, default="draft")
    allowed_copy = fields.Text("Allowed wording")
    limitations = fields.Text()
    internal_source = fields.Char(
        "Evidence references", groups="spk_website_v2.group_spk_website_editor",
        help="Internal source references. Never rendered on the public site.")
    owner_role = fields.Selection(OWNER_ROLES, string="Owner")
    reviewed_at = fields.Date("Verified on")

    _sql_constraints = [
        ("code_unique", "unique(code)", "A claim code is unique."),
    ]

    @api.depends("code", "name")
    def _compute_display_label(self):
        for claim in self:
            claim.display_label = "%s %s" % (claim.code or "", claim.name or "")

    def write(self, vals):
        if "code" in vals and any(claim.code != vals["code"] for claim in self):
            raise UserError(self.env._("A claim code is permanent. Withdraw the claim and create a new one instead."))
        return super().write(vals)

    def allows_public_rows(self):
        self.ensure_one()
        return self.publication in PUBLIC_STATES
