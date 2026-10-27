# -*- coding: utf-8 -*-
"""Published resources: the buyer guides (/resources/<slug>) and the
articles kept from the Webflow blog (/post/<slug>).

A small dedicated model rather than website_blog, which the deployment does
not use. Editors change the text; only a publisher changes what is published.
"""

import re

from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..site_content import POST_PREFIX, RESOURCE_PREFIX, ROUTES

KINDS = [
    ("guide", "Buyer guide"),
    ("post", "Archived article"),
]
CATEGORIES = [
    ("getting_started", "Getting started"),
    ("cards_devices", "Cards and devices"),
    ("networks_automation", "Networks and automation"),
    ("operating", "Operating your system"),
    ("insights", "Insights"),
]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PUBLIC_FIELDS = ("kind", "slug", "name", "seo_title", "description", "direct_answer", "body", "category",
                 "hero_image", "hero_alt", "author_name", "published_on", "modified_on", "reviewed_on")


class SpkWebsiteResource(models.Model):
    _name = "spk.website.resource"
    _description = "SmartphoneKey website resource"
    _order = "kind, sequence, published_on desc, id"

    sequence = fields.Integer(default=10)
    kind = fields.Selection(KINDS, required=True, default="guide")
    slug = fields.Char(required=True)
    name = fields.Char("Title", required=True)
    seo_title = fields.Char("SEO title", required=True)
    description = fields.Char("Meta description", required=True)
    direct_answer = fields.Text(help="The 50-80 word answer shown first on the page.")
    body = fields.Html(sanitize=True)
    category = fields.Selection(CATEGORIES, required=True)
    hero_image = fields.Char(help="Path of an image shipped with the module.")
    hero_alt = fields.Char("Image description")
    related_paths = fields.Char(help="Comma-separated site paths shown as related pages.")
    source_links = fields.Text(help="One reference per line: label | https://...")
    author_name = fields.Char("Attribution", required=True, default="SmartphoneKey product team")
    published_on = fields.Date(required=True)
    modified_on = fields.Date(help="Set only when the content changes substantively.")
    reviewed_on = fields.Date("Reviewed on")
    is_published = fields.Boolean("Published", default=False, copy=False)
    path = fields.Char(compute="_compute_path")

    _sql_constraints = [
        ("kind_slug_unique", "unique(kind, slug)", "A resource slug is unique within its kind."),
    ]

    @api.depends("kind", "slug")
    def _compute_path(self):
        for resource in self:
            prefix = POST_PREFIX if resource.kind == "post" else RESOURCE_PREFIX
            resource.path = prefix + (resource.slug or "")

    @api.constrains("slug")
    def _check_slug(self):
        for resource in self:
            if not SLUG_RE.match(resource.slug or ""):
                raise ValidationError(self.env._("A slug uses lowercase letters, digits and single hyphens."))

    @api.constrains("related_paths")
    def _check_related_paths(self):
        for resource in self:
            for path in resource._related_path_list():
                if path not in ROUTES and not path.startswith((RESOURCE_PREFIX, POST_PREFIX)):
                    raise ValidationError(self.env._("Related page %s is not a page of the site.", path))

    @api.model_create_multi
    def create(self, vals_list):
        if any(vals.get("is_published") for vals in vals_list):
            self._check_publisher()
        return super().create(vals_list)

    def write(self, vals):
        if "is_published" in vals:
            self._check_publisher()
        return super().write(vals)

    def _check_publisher(self):
        if not self.env.su and not self.env.user.has_group("spk_website_v2.group_spk_website_publisher"):
            raise AccessError(self.env._("Only a website publisher can publish or unpublish a resource."))

    def _related_path_list(self):
        self.ensure_one()
        return [path.strip() for path in (self.related_paths or "").split(",") if path.strip()]

    def _source_link_list(self):
        self.ensure_one()
        links = []
        for line in (self.source_links or "").splitlines():
            label, _sep, url = line.partition("|")
            if url.strip().startswith("https://"):
                links.append((label.strip(), url.strip()))
        return links

    @api.model
    def _public_resource(self, kind, slug):
        """One published resource as a dict of public fields, or None."""
        resource = self.sudo().search([("kind", "=", kind), ("slug", "=", slug), ("is_published", "=", True)],
                                      limit=1)
        return resource._public_values() if resource else None

    @api.model
    def _public_list(self, kind):
        resources = self.sudo().search([("kind", "=", kind), ("is_published", "=", True)])
        return [resource._public_values() for resource in resources]

    def _public_values(self):
        self.ensure_one()
        values = {field: self[field] or False for field in PUBLIC_FIELDS}
        values["path"] = self.path
        values["related"] = [(ROUTES[path]["label"], path) if path in ROUTES else (path, path)
                             for path in self._related_path_list()]
        values["sources"] = self._source_link_list()
        values["category_label"] = dict(CATEGORIES).get(self.category, "")
        return values
