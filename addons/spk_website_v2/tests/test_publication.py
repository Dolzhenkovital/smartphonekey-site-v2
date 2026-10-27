# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo.tests import new_test_user, tagged

from .common import SiteCase


@tagged("post_install", "-at_install")
class TestPublication(SiteCase):
    """A22: an edited technical row goes back to review; unverified claims stay gated."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.editor = new_test_user(cls.env, "spk_editor", groups="base.group_user,spk_website_v2.group_spk_website_editor")
        cls.publisher = new_test_user(cls.env, "spk_publisher",
                                      groups="base.group_user,spk_website_v2.group_spk_website_publisher")
        cls.row = cls.env.ref("spk_website_v2.compat_mifare_classic")

    def test_editing_a_published_row_sends_it_back_to_review(self):
        Rows = self.env["spk.website.compatibility"]
        self.assertIn("MIFARE Classic", [row["name"] for row in Rows._public_rows("cards")])
        self.row.with_user(self.editor).write({"limitations": "Edited wording awaiting review."})
        self.assertEqual(self.row.state, "review")
        self.assertNotIn("MIFARE Classic", [row["name"] for row in Rows._public_rows("cards")])
        self.assertNotIn(b"Edited wording awaiting review.", self.get("/compatibility").content)

        with self.assertRaises(AccessError):
            self.row.with_user(self.editor).action_publish()
        self.row.with_user(self.publisher).action_publish()
        self.assertEqual(self.row.state, "published")
        self.assertEqual(self.row.verified_at, self.row.verified_at.today())
        body = self.get("/compatibility").content.decode()
        self.assertIn("Edited wording awaiting review.", body)
        self.assertIn("Reviewed %d " % self.row.verified_at.day, body)

    def test_rows_of_ungated_claims_cannot_be_published(self):
        distance = self.env.ref("spk_website_v2.compat_reader_link_distance")
        with self.assertRaises(UserError):
            distance.with_user(self.publisher).action_publish()
        body = self.get("/compatibility").content
        self.assertNotIn(b"Distance between readers", body)
        # C13, published on the owner's instruction of 2026-10-27.
        self.assertIn(b"Reader Thread roles", body)
        self.assertIn(b"No separate firmware version is needed for either role.", body)

    def test_private_evidence_never_reaches_the_page(self):
        body = self.get("/compatibility").content
        for internal in (b"P05", b"P07", b"evidence_ref", b"internal_source", b"AP-379"):
            self.assertNotIn(internal, body)

    def test_public_user_has_no_model_access(self):
        public = self.env.ref("base.public_user")
        for model in ("spk.website.claim", "spk.website.compatibility", "spk.website.resource",
                      "spk.website.team.member", "spk.website.enquiry.attempt"):
            with self.assertRaises(AccessError):
                self.env[model].with_user(public).search([])

    def test_claim_codes_are_permanent(self):
        claim = self.env.ref("spk_website_v2.claim_c05")
        with self.assertRaises(UserError):
            claim.with_user(self.publisher).write({"code": "C99"})

    def test_only_publishers_publish_resources(self):
        guide = self.env.ref("spk_website_v2.resource_offline")
        with self.assertRaises(AccessError):
            guide.with_user(self.editor).write({"is_published": False})
        guide.with_user(self.editor).write({"direct_answer": guide.direct_answer})
        guide.with_user(self.publisher).write({"is_published": False})
        self.assertEqual(self.get("/resources/access-control-when-offline").status_code, 404)
