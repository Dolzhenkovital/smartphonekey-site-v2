# -*- coding: utf-8 -*-
import uuid
from unittest.mock import patch

from lxml import html as lxml_html

from odoo.tests import tagged
from odoo.tools import mute_logger

from ..models.crm_lead import CONFLICT, DUPLICATE, CrmLead
from ..models.enquiry_attempt import MAX_ATTEMPTS
from ..rendering import PREVIEW_PARAM
from .common import SiteCase

ENDPOINT = "/website/spk/enquiry"
JSON = {"Accept": "application/json"}


@tagged("post_install", "-at_install")
class TestEnquiry(SiteCase):

    def setUp(self):
        super().setUp()
        self.Lead = self.env["crm.lead"].sudo().with_context(active_test=False)
        # Each test starts with a clean throttle window.
        self.env["spk.website.enquiry.attempt"].sudo().search([]).unlink()

    def form(self, **overrides):
        """A fresh contact form: its CSRF token and submission ID, plus valid values."""
        _response, doc = self.page("/contact")
        values = {
            "csrf_token": doc.xpath("//input[@name='csrf_token']/@value")[0],
            "submission_id": doc.xpath("//input[@name='submission_id']/@value")[0],
            "source_path": "/find-your-setup",
            "name": "Test Visitor",
            "email": "test.visitor@example.com",
            "enquiry_type": "project",
            "company": "Example Properties",
            "role": "property_manager",
            "sites": "two_to_ten",
            "doors": "six_to_twentyfive",
            "connection": "wifi",
            "region": "Example region",
            "details": "Synthetic test enquiry.",
        }
        values.update(overrides)
        return values

    def post(self, data, json=True):
        return self.url_open(ENDPOINT, data=data, headers=JSON if json else None, allow_redirects=False)

    def leads(self, submission_id):
        return self.Lead.search([("spk_submission_id", "=", submission_id)])

    def test_valid_enquiry_creates_one_lead_with_its_context(self):
        data = self.form()
        response = self.post(list(data.items()) + [("interests", "cards"), ("interests", "visitors")])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True, "status": "created"})
        lead = self.leads(data["submission_id"])
        self.assertEqual(len(lead), 1)
        self.assertEqual(lead.name, "Website — Project planning — Example Properties")
        self.assertEqual((lead.contact_name, lead.email_from, lead.partner_name),
                         ("Test Visitor", "test.visitor@example.com", "Example Properties"))
        self.assertEqual((lead.spk_enquiry_type, lead.spk_role, lead.spk_sites, lead.spk_doors, lead.spk_connection),
                         ("project", "property_manager", "two_to_ten", "six_to_twentyfive", "wifi"))
        self.assertEqual(lead.spk_interests, "cards,visitors")
        self.assertEqual(lead.spk_source_path, "/find-your-setup")
        website = self.env["website"].get_current_website()
        self.assertEqual(lead.team_id, website.crm_default_team_id)
        self.assertEqual(lead.company_id, website.company_id)

    def test_retries_and_concurrent_duplicates_create_one_lead(self):
        """A10: double click, timeout-then-retry: one lead, the same answer."""
        data = self.form()
        first = self.post(data)
        second = self.post(data)
        self.assertEqual(first.json()["ok"], True)
        self.assertEqual(second.json(), {"ok": True, "status": "duplicate"})
        self.assertEqual(len(self.leads(data["submission_id"])), 1)
        # The same ID with other content is refused, not merged or duplicated.
        changed = dict(data, details="Something else")
        conflict = self.post(changed)
        self.assertEqual(conflict.status_code, 409)
        self.assertEqual(len(self.leads(data["submission_id"])), 1)

    def test_insert_race_is_resolved_by_the_unique_index(self):
        """A concurrent request committed the same submission between our check and our insert."""
        data = self.form()
        self.assertTrue(self.post(data).json()["ok"])
        payload = {
            "name": "Test Visitor", "email": "test.visitor@example.com", "enquiry_type": "project",
            "company": "Example Properties", "region": "Example region", "details": "Synthetic test enquiry.",
            "phone": "", "role": "property_manager", "sites": "two_to_ten", "doors": "six_to_twentyfive",
            "connection": "wifi", "interests": [], "source_path": "/find-your-setup",
            "submission_id": data["submission_id"], "lang": "en_US",
        }
        website = self.env["website"].get_current_website()
        Lead = self.env["crm.lead"]
        original_search = type(Lead).search

        def blind_search(records, domain, *args, **kwargs):
            # Our snapshot does not see the other request's lead yet.
            if any(isinstance(term, (list, tuple)) and term[0] == "spk_submission_id" for term in domain):
                return records.browse()
            return original_search(records, domain, *args, **kwargs)

        def committed_digest(records, submission_id):
            records.env.cr.execute("SELECT spk_submission_digest FROM crm_lead WHERE spk_submission_id = %s",
                                   [submission_id])
            row = records.env.cr.fetchone()
            return row[0] if row else None

        # The unique index rejects the second insert, and Odoo logs that query at error level.
        with patch.object(type(Lead), "search", blind_search), mute_logger("odoo.sql_db"), \
                patch.object(CrmLead, "_spk_committed_enquiry_digest", committed_digest):
            same, _lead = Lead._spk_submit_website_enquiry(dict(payload), website)
            changed, _lead = Lead._spk_submit_website_enquiry(dict(payload, details="Changed"), website)
        self.assertEqual(same, DUPLICATE)
        self.assertEqual(changed, CONFLICT)
        self.assertEqual(len(self.leads(data["submission_id"])), 1)

    def test_missing_csrf_token_is_rejected(self):
        data = self.form()
        del data["csrf_token"]
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.leads(data["submission_id"]))

    def test_invalid_and_hostile_input(self):
        """A11: overlong values, HTML, server-owned fields and the honeypot."""
        data = self.form(name="x" * 121)
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json()["fields"])
        self.assertFalse(self.leads(data["submission_id"]))

        data = self.form(email="not-an-email", enquiry_type="sales", sites="999")
        fields = self.post(data).json()["fields"]
        self.assertEqual(set(fields), {"email", "enquiry_type", "sites"})

        admin = self.env.ref("base.user_admin")
        other_team = self.env["crm.team"].sudo().create({"name": "Not the website team"})
        data = self.form(details="<script>alert(1)</script><b>bold</b>")
        hostile = dict(data, user_id=admin.id, team_id=other_team.id, company_id=99, stage_id=1,
                       email_to="attacker@example.com", spk_submission_digest="x")
        self.assertTrue(self.post(hostile).json()["ok"])
        lead = self.leads(data["submission_id"])
        self.assertNotEqual(lead.user_id, admin)
        self.assertNotEqual(lead.team_id, other_team)
        self.assertNotIn("<script>", lead.description)
        self.assertIn("&lt;script&gt;", lead.description)

        data = self.form(spk_website_check="https://spam.example")
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.leads(data["submission_id"]))

    def test_without_javascript(self):
        """The plain form POST: a redirect after success, the form again after an error."""
        data = self.form()
        response = self.post(data, json=False)
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.headers["Location"].endswith("/thank-you"))
        doc = lxml_html.fromstring(self.get("/thank-you").content)
        self.assertEqual(doc.xpath("//h1")[0].text_content(), "Your enquiry has been received.")
        doc = lxml_html.fromstring(self.get("/thank-you").content)
        self.assertEqual(doc.xpath("//h1")[0].text_content(), "No enquiry to confirm")

        data = self.form(email="nope", name="<b>Visitor</b>")
        response = self.post(data, json=False)
        self.assertEqual(response.status_code, 400)
        doc = lxml_html.fromstring(response.content)
        self.assertTrue(doc.xpath("//div[@data-spk-error-summary]//a[@href='#field-email']"))
        self.assertEqual(doc.xpath("//input[@name='name']/@value"), ["<b>Visitor</b>"])
        self.assertNotIn(b"<b>Visitor</b>", response.content)
        self.assertEqual(doc.xpath("//input[@name='submission_id']/@value"), [data["submission_id"]])

    def test_throttle(self):
        for _index in range(MAX_ATTEMPTS):
            self.assertTrue(self.post(self.form()).json()["ok"])
        data = self.form()
        response = self.post(data)
        self.assertEqual(response.status_code, 429)
        self.assertFalse(self.leads(data["submission_id"]))

    def test_preview_never_stores(self):
        self.env["ir.config_parameter"].sudo().set_param(PREVIEW_PARAM, "True")
        try:
            data = self.form()
            response = self.post(data)
            self.assertEqual(response.status_code, 503)
            self.assertFalse(self.leads(data["submission_id"]))
            _response, doc = self.page("/contact")
            self.assertTrue(doc.xpath("//button[@data-spk-submit][@disabled]"))
        finally:
            self.env["ir.config_parameter"].sudo().set_param(PREVIEW_PARAM, "False")

    def test_public_user_cannot_read_leads(self):
        public = self.env.ref("base.public_user")
        with self.assertRaises(Exception):
            self.env["crm.lead"].with_user(public).search([])

    def test_bad_submission_id(self):
        data = self.form(submission_id=uuid.uuid4().hex.upper())
        self.assertEqual(self.post(data).status_code, 400)
