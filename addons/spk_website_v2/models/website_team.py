# -*- coding: utf-8 -*-
"""The team pages kept from the Webflow site (/team/<slug>) and the About list."""

from odoo import api, fields, models
from odoo.exceptions import AccessError
from odoo.tools.translate import html_translate

PUBLIC_FIELDS = ("slug", "name", "job_title", "bio", "linkedin_url", "photo", "photo_alt", "is_advisor")


class SpkWebsiteTeamMember(models.Model):
    _name = "spk.website.team.member"
    _description = "SmartphoneKey website team member"
    _order = "is_advisor, sequence, id"

    sequence = fields.Integer(default=10)
    slug = fields.Char(required=True)
    name = fields.Char(required=True)
    job_title = fields.Char(required=True, translate=True)
    is_advisor = fields.Boolean("Advisor")
    bio = fields.Html(sanitize=True, translate=html_translate)
    linkedin_url = fields.Char("LinkedIn profile")
    photo = fields.Char(help="Path of a photo shipped with the module.")
    photo_alt = fields.Char("Photo description", translate=True)
    role_checked_on = fields.Date(
        "Role confirmed on", help="Set when the current role has been confirmed with the person. "
                                  "Internal; shown in the release checklist, not on the site.")
    is_published = fields.Boolean("Published", default=False, copy=False)

    _sql_constraints = [
        ("slug_unique", "unique(slug)", "A team member slug is unique."),
    ]

    def write(self, vals):
        if "is_published" in vals and not self.env.su \
                and not self.env.user.has_group("spk_website_v2.group_spk_website_publisher"):
            raise AccessError(self.env._("Only a website publisher can publish or unpublish a team page."))
        return super().write(vals)

    @api.model
    def _public_member(self, slug):
        member = self.sudo().search([("slug", "=", slug), ("is_published", "=", True)], limit=1)
        return {field: member[field] or False for field in PUBLIC_FIELDS} if member else None

    @api.model
    def _public_list(self):
        members = self.sudo().search([("is_published", "=", True)])
        return [{field: member[field] or False for field in PUBLIC_FIELDS} for member in members]
