# -*- coding: utf-8 -*-
"""The site recommendations result and the contact form's prefill note.

Both are server-rendered from the enum query string, so they work without
JavaScript; setup_guide.js fills the same elements in place. The Ukrainian
copy is not translated yet, so the contact test asserts structure (data
attributes, selected options), not Ukrainian text."""
from odoo.tests import tagged

from .. import setup_guide
from .. import site_content as content
from .common import SiteCase

SELECTION_URL = "/find-your-setup?role=property_manager&sites=two_to_ten&connection=wifi&interests=cards"


def words(node):
    return " ".join(node.text_content().split())


@tagged("post_install", "-at_install")
class TestSetupResult(SiteCase):

    def test_selection_labels_follow_form_order(self):
        selection = {"interests": ["cards", "wallets"], "connection": "both", "role": "owner", "doors": "one_to_five"}
        self.assertEqual(setup_guide.selection_labels(selection),
                         ["Building owner", "1 to 5 doors", "Both", "NFC cards", "Wallet keys"])
        self.assertEqual(setup_guide.selection_labels({}), [])
        # Labels go through the translator; values outside the allowlist are left out.
        self.assertEqual(setup_guide.selection_labels({"sites": "one", "role": "bogus"}, t=str.upper), ["1 SITE"])
        result = setup_guide.result_for({"connection": "wifi", "sites": "one"})
        self.assertEqual(result["summary"], ["1 site", "Wi-Fi"])
        self.assertIsNone(setup_guide.result_for({"sites": "one"}))

    def test_result_has_every_field_without_javascript(self):
        _response, doc = self.page(SELECTION_URL)
        result = doc.xpath("//section[@id='setup-result'][@data-spk-setup-result]")[0]
        self.assertEqual(result.get("tabindex"), "-1")
        self.assertEqual(words(result.xpath(".//h2")[0]), "Recommendations for your site")
        # The empty state is hidden, the fields are shown.
        self.assertEqual(result.xpath(".//*[@data-spk-result-empty]")[0].get("hidden"), "hidden")
        body = result.xpath(".//*[@data-spk-result-body]")[0]
        self.assertIsNone(body.get("hidden"))
        # The fields, in order.
        self.assertEqual([words(label) for label in body.xpath(".//dt")], [
            "Your selection", "Recommendation", "Why", "Still to check on site", "Guides for your selection"])

        # Your selection: the four chosen labels in form order, then the way back to the form.
        chips = [words(chip) for chip in body.xpath(".//*[@data-spk-result-summary]/li")]
        self.assertEqual(chips, ["Property manager", "2 to 10 sites", "Wi-Fi", "NFC cards"])
        change = body.xpath(".//a[@href='#guide-form-title']")
        self.assertEqual([words(link) for link in change], ["Change answers"])
        self.assertTrue(doc.xpath("//*[@id='guide-form-title']"))

        # Recommendation and why.
        self.assertEqual(words(body.xpath(".//*[@data-spk-result-advice]")[0]), content.SETUP_CONNECTION_ADVICE["wifi"])
        self.assertEqual(words(body.xpath(".//*[@data-spk-result-why]")[0]),
                         "Each reader needs a reliable connection at its own position to receive access "
                         "changes and report events.")

        # Still to check on site: the rules of this selection, and none of the cellular ones.
        items = [words(item) for item in body.xpath(".//*[@data-spk-result-items]/li")]
        for prefix in (
                "List each door with its lock hardware",
                "Check Wi-Fi coverage at every planned reader position",
                "Decide how each site will be set up and who administers it locally.",
                "Map residents, staff and contractors to the doors each group needs.",
                "Confirm the exact card product with us."):
            self.assertEqual(len([item for item in items if item.startswith(prefix)]), 1, prefix)
        self.assertEqual(len(items), 5, items)
        self.assertFalse([item for item in items if "cellular coverage" in item])

        # Guides for your selection.
        links = {words(link): link.get("href") for link in body.xpath(".//*[@data-spk-result-links]//a")}
        self.assertEqual(links, {
            "LTE or Wi-Fi: what fits your site?": "/resources/lte-vs-wifi-access-control",
            "Managing access across sites": "/platform/access-management",
            "Access control for property teams": "/solutions/property-managers",
            "Which NFC cards can SmartphoneKey program?": "/resources/mifare-classic-desfire-ev3",
        })
        self.assertEqual(words(body.xpath(".//*[@data-spk-result-links-title]")[0]), "Guides for your selection")

        # The contact link keeps the enum choices (and nothing else); the help text says so.
        contact = body.xpath(".//a[@data-spk-result-contact]")
        self.assertEqual(len(contact), 1)
        self.assertEqual(words(contact[0]), "Discuss these recommendations")
        self.assertEqual(contact[0].get("href"), "/contact?interest=project&role=property_manager"
                                                 "&sites=two_to_ten&connection=wifi&interests=cards")
        self.assertIn("Your answers are copied into the enquiry form, where you can change them.", words(body))

        # The other action; "Keep exploring" is gone.
        self.assertTrue(result.xpath(".//a[@href='/compatibility'][normalize-space()='Check compatibility']"))
        self.assertNotIn("Keep exploring", words(result))

    def test_result_stays_empty_until_a_connection_is_chosen(self):
        _response, doc = self.page("/find-your-setup?role=owner&sites=one")
        result = doc.xpath("//section[@id='setup-result']")[0]
        empty = result.xpath(".//*[@data-spk-result-empty]")[0]
        self.assertIsNone(empty.get("hidden"))
        self.assertIn("Choose the connection at your doors to see recommendations.", words(empty))
        self.assertEqual([link.get("href") for link in empty.xpath(".//a")], ["/contact?interest=project"])
        self.assertEqual([words(link) for link in empty.xpath(".//a")], ["Discuss your project"])
        self.assertEqual(result.xpath(".//*[@data-spk-result-body]")[0].get("hidden"), "hidden")
        self.assertFalse(result.xpath(".//*[@data-spk-result-summary]/li"))
        self.assertFalse(result.xpath(".//*[@data-spk-result-items]/li"))
        self.assertFalse(result.xpath(".//*[@data-spk-result-links]//a"))
        # The scripted page still finds the link it updates.
        self.assertEqual(result.xpath(".//a[@data-spk-result-contact]/@href"), ["/contact?interest=project"])

    def test_home_tool_site_choice_joins_the_connection(self):
        """F22: "See full recommendations" never returns less than the compact tool."""
        multi_site = "Decide how each site will be set up and who administers it locally."
        installer = "Plan the installation, the handover to the customer's site administrators"
        cases = (
            # (query, chips, an item that must be there, an item that must not)
            ("site=portfolio&connection=cellular", ["2 to 10 sites", "Cellular (LTE)"], multi_site, installer),
            ("site=partner&connection=wifi", ["Installer or integrator", "Wi-Fi"], installer, multi_site),
            ("site=property&connection=wifi", ["1 site", "Wi-Fi"], "List each door with its lock hardware", multi_site),
        )
        for query, chips, expected, absent in cases:
            _response, doc = self.page("/find-your-setup?" + query)
            result = doc.xpath("//section[@id='setup-result']")[0]
            self.assertIsNone(result.xpath(".//*[@data-spk-result-body]")[0].get("hidden"), query)
            self.assertEqual([words(chip) for chip in result.xpath(".//*[@data-spk-result-summary]/li")], chips, query)
            items = [words(item) for item in result.xpath(".//*[@data-spk-result-items]/li")]
            self.assertTrue([item for item in items if item.startswith(expected)], "%s lacks %r" % (query, expected))
            self.assertFalse([item for item in items if item.startswith(absent)], "%s has %r" % (query, absent))
            # The form shows the mapped choice, and the contact link carries it.
            field, value = ("role", "integrator") if "partner" in query else (
                "sites", "two_to_ten" if "portfolio" in query else "one")
            self.assertEqual(doc.xpath("//input[@name='%s'][@checked]/@value" % field), [value], query)
            self.assertIn("%s=%s" % (field, value), result.xpath(".//a[@data-spk-result-contact]/@href")[0])
        # An answer given on this page wins over the home tool's site choice.
        _response, doc = self.page("/find-your-setup?site=partner&connection=wifi&role=owner&interests=cards")
        chips = [words(chip) for chip in doc.xpath("//*[@data-spk-result-summary]/li")]
        self.assertEqual(chips, ["Building owner", "Wi-Fi", "NFC cards"])
        _response, doc = self.page("/find-your-setup?site=portfolio&connection=wifi&doors=one_to_five")
        self.assertEqual([words(chip) for chip in doc.xpath("//*[@data-spk-result-summary]/li")], ["1 to 5 doors", "Wi-Fi"])
        # Interests survive the mapping; an unknown site is ignored.
        _response, doc = self.page("/find-your-setup?site=portfolio&connection=wifi&interests=wallets")
        self.assertEqual([words(chip) for chip in doc.xpath("//*[@data-spk-result-summary]/li")],
                         ["2 to 10 sites", "Wi-Fi", "Wallet keys"])
        _response, doc = self.page("/find-your-setup?site=bogus&connection=wifi")
        self.assertEqual([words(chip) for chip in doc.xpath("//*[@data-spk-result-summary]/li")], ["Wi-Fi"])

    def test_connection_basics_reuse_the_advice(self):
        _response, doc = self.page("/find-your-setup")
        section = doc.xpath("//section[@aria-labelledby='basics-title']")[0]
        self.assertEqual(words(section.xpath(".//h2")[0]), "Choosing the connection")
        descriptions = [words(item) for item in section.xpath(".//dd")]
        self.assertEqual(descriptions, [content.SETUP_CONNECTION_ADVICE[key] for key in ("wifi", "cellular", "unsure")])

    def test_contact_prefill_note_follows_the_recommendations(self):
        # Enum choices from the recommendations, in the visitor's language.
        _response, doc = self.page("/uk/contact?interest=project&role=owner&connection=wifi")
        note = doc.xpath("//p[@data-spk-prefill-note]")
        self.assertEqual(len(note), 1)
        self.assertIn("note", note[0].get("class").split())
        # The note comes before the form, and the choices are kept in it.
        self.assertTrue(note[0].xpath("following::form[@data-spk-enquiry]"))
        self.assertEqual(doc.xpath("//select[@name='enquiry_type']/option[@selected]/@value"), ["project"])
        self.assertEqual(doc.xpath("//select[@name='role']/option[@selected]/@value"), ["owner"])
        self.assertEqual(doc.xpath("//select[@name='connection']/option[@selected]/@value"), ["wifi"])
        self.assertFalse(doc.xpath("//select[@name='sites']/option[@selected]"))

        # Odoo remembers the last language in a cookie; the rest is English again.
        self.opener.cookies.clear()
        # Interests listed in the query count as the tool's choices too.
        _response, doc = self.page("/contact?interests=cards&interests=wallets")
        self.assertEqual(len(doc.xpath("//p[@data-spk-prefill-note]")), 1)
        self.assertEqual(doc.xpath("//input[@name='interests'][@checked]/@value"), ["cards", "wallets"])

        # No note without the tool's choices: a plain visit, a link from a page of the site
        # (interest=automation ticks an interest itself), or values outside the allowlist.
        for path in ("/contact", "/uk/contact", "/contact?interest=partner", "/contact?interest=automation",
                     "/contact?role=bogus&sites=999&interests=bogus"):
            self.opener.cookies.clear()
            _response, doc = self.page(path)
            self.assertFalse(doc.xpath("//p[@data-spk-prefill-note]"), path)
        self.opener.cookies.clear()
        _response, doc = self.page("/contact?interest=automation")
        self.assertEqual(doc.xpath("//input[@name='interests'][@checked]/@value"), ["automation"])
