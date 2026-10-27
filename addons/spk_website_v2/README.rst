==========================
SmartphoneKey Website 2.0
==========================

smartphonekey.com 2.0: the access control management platform site, built on
the AP-428 Webflow port (``spk_website``) instead of replacing it.

* Every page is a QWeb template on ``spk_website_v2.layout``, a bare
  ``web.layout`` document like the baseline's, with its own scoped CSS bundle
  (``spk_website_v2.assets_site``) and three small deferred scripts. Nothing
  loads on the portal, the login or the instruction site.
* Routes, navigation, calls to action, the enquiry form's allowed values, the
  setup-guide rules and the decision for every Webflow URL live in
  ``site_content.py``; metadata, structured data and the sitemap come from it.
* ``/`` keeps the AP-429 switch ("Use SmartphoneKey site as homepage"). The
  baseline's Webflow URLs are retained in the 2.0 shell or answered with a
  301; ``/adminpanel``, ``/referral-program`` and ``/spk-website/form`` stay
  with the baseline; the instruction site stays with ``smartphonekey``.
* ``spk_website_v2.enabled`` set to ``False`` hands every URL back to the
  baseline (rollback); ``spk_website_v2.preview_mode`` makes a review copy:
  banner, noindex and a form that never stores.
* Enquiries: ``POST /website/spk/enquiry`` (CSRF, allowlisted fields, honeypot,
  per-visitor throttle with a daily keyed hash of the address, the website
  forms' captcha check). A per-form submission ID with a unique index makes
  retries and concurrent duplicates answer the first result without a second
  lead. Success is shown only once the lead exists.
* Content operations: ``spk.website.claim`` (claim register),
  ``spk.website.compatibility`` (rows; editing a published row sends it back to
  review), ``spk.website.resource`` (buyer guides and archived articles) and
  ``spk.website.team.member``, with editor and publisher groups. Public pages
  read them through explicit public-field projections.
* Unknown public URLs answer a real 404 in the 2.0 shell.

The archived articles, team pages and legal text were imported once from the
Webflow export by ``tools/import_legacy_content.py`` and are maintained here.
