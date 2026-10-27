# Implementation status

Last update: 27 October 2026. State: **ready for review**, not deployed. All six phases are implemented and checked in a local Odoo 18 test instance; the static review copy is published separately on GitHub Pages.

## Where the work lives

| Part | Location |
|---|---|
| Odoo 18 addon | [`addons/spk_website_v2`](addons/spk_website_v2) |
| Local test environment | [`dev/`](dev) (Docker: Odoo 18 + PostgreSQL 16, baseline mounted read-only) |
| Tools | [`tools/`](tools): legacy import, static export and link check, concurrency check, screenshots |
| Registers | [`registers/`](registers): routes, the 34 legacy URLs, claim usage |
| QA evidence | [`QA-REPORT.md`](QA-REPORT.md), [`qa/`](qa) |
| Release and rollback | [`RELEASE-CHECKLIST.md`](RELEASE-CHECKLIST.md) |
| Static review copy | [`preview/`](preview), published by `.github/workflows/pages.yml` |

## Integration decision

The AP-428 Webflow port (`spk_website`, with the AP-429 homepage switch) exists on the spk-odoo branches and is deployed on spkey.odoo.com. Rather than rewrite it, `spk_website_v2` **depends on it and extends it**:

* `/` extends `SpkWebsiteHome.index`, so "Use SmartphoneKey site as homepage" and a website Homepage URL still decide what `/` shows.
* The baseline's Webflow URLs go through an override of its `page`, `post`, `team_member` and `/404` handlers: retained in the 2.0 shell or answered with a 301.
* Untouched and still served by the baseline: `/adminpanel` (portal entry, redirects to `/my`), `/referral-program` (noindex) and its form endpoint `/spk-website/form`.
* Untouched and served by `smartphonekey`: `/guide-for-usage-and-installation` and `/instructions/*`, in their languages.
* Rollback switch: system parameter `spk_website_v2.enabled` = `False` hands every URL back to the baseline without touching data (tested).

To ship it, copy `addons/spk_website_v2` into spk-odoo `addons/` on a branch named for its Jira task, add `spk_website_v2` to the deployment, and follow that repository's PR rules (changelog entry, `> Guide: n/a`, lint gates).

## Phases

| Phase | Done | Exit evidence |
|---|---|---|
| 1 Baseline, evidence, routes, assets | Baseline inspected (AP-428/AP-429 code, live spkey.odoo.com, mirror, export); claim, route and redirect registers; genuine assets only (logo, reader photo, team photos, article images, four certificate documents) | `registers/`, importer `tools/import_legacy_content.py` (reads the public export, never `export/private` or `.env`) |
| 2 Tokens, layout, home | Locked tokens and reference CSS ported to one scoped SCSS file; header, footer, seven-section home; working two-field setup tool | Screenshots at 8 sizes, keyboard and reduced-motion checks |
| 3 Pages and setup guide | 15 new routes, 4 buyer guides, retained certifications/apps/legal/posts/team in the new shell; deterministic setup guide (server and script share one rule table) | `test_routes`, crawl of every page, no-JS screenshots |
| 4 CRM and content operations | `POST /website/spk/enquiry`: allowlist, CSRF, honeypot, throttle, captcha hook, idempotent submission ID with a unique index, honest errors, `/thank-you` only after persistence; claim register, compatibility rows with review/publish, resources and team as editable records with editor/publisher groups | `test_enquiry`, `test_publication`, real concurrency run |
| 5 Search and migration | Canonicals, metadata, Open Graph, JSON-LD from the same data, own sitemap and robots, 34 legacy URLs handled, staging/preview noindex | `test_seo`, `test_migration`, `qa/robots-*.txt`, `qa/sitemap-*.xml` |
| 6 QA and release preparation | Tests, lint, Hallmark render lint, screenshots, static copy check, QA report, release/rollback checklist | `QA-REPORT.md` |

`llms.txt` (optional P1) was **not** added: the brief allows it only once the core has passed, and the core has not yet been accepted on a deployed environment (A20).

## Fallbacks in effect

* No range report: no distance anywhere; "coverage depends on the building, placement and radio conditions".
* No hardware-role matrix: "confirm model and firmware" for Matter and Thread roles; the role row stays in review.
* Shared uplink: FAQ wording with "confirmed for the installed hardware"; the Matter guide topology is labelled as an example.
* AI Concierge v2: availability-enquiry wording.
* Certifications: document links with what each document states; no badges.
* No booking URL configured: no booking link (the option appears only for an HTTPS URL on an allowed host, set in `spk_website_v2.booking_url`).
* No genuine Admin Panel screens: labelled conceptual diagram and tables; no product screenshots drawn.
* Marketing consent not implemented: no opt-in checkbox and no analytics loader.

## Open items (owner role)

1. Design owner: confirm the long-document reading of Hallmark rule 58 for deep pages, or supply shorter copy (QA D1).
2. Hardware/firmware: reader role matrix (C13), uplink topology (C14), range report (C15), FCC/ISED record check (C20).
3. Product owner: AI Concierge v2 release status (C17); ChatGPT app description; referral programme keep or retire.
4. Marketing: archived article review; current team roles; analytics loader and consent decision; font licence for self-hosting.
5. Operations: who receives website leads (website sales team and salesperson in Website settings).
6. Engineering: merge into spk-odoo, run its gates and `make test` on Odoo.sh, verify on stage, then the release checklist.
