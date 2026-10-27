# Implementation status

Last update: 27 October 2026 (revision after the owner's assessment "different but not better"). State: **ready for review**, local only, not deployed. The addon is at 18.0.3.0.0; the GitHub Pages review copy is regenerated from the updated sources in this working tree (see QA-REPORT.md for what was checked and how).

## Where the work lives

| Part | Location |
|---|---|
| Odoo 18 addon | [`addons/spk_website_v2`](addons/spk_website_v2) |
| Local test environment | [`dev/`](dev) (Docker: Odoo 18 + PostgreSQL 16, baseline mounted read-only) |
| Tools | [`tools/`](tools): legacy import, static export and link check, concurrency check, screenshots (`capture_screens.mjs`), translation build (`i18n_build.py`), translation checks (`i18n_check.py`), soft hyphens (`i18n_soft_hyphens.py`) |
| Registers | [`registers/`](registers): routes, the 34 legacy URLs, claim usage |
| Content and design sources | `../docs/site-v2/04-COPY-DECK-EN.md` (English deck, revision 2.2), `GLOSSARY.md`, `LOCALE-BRIEF.md`, `DESIGN.md` (design contract), `concepts/` (the two layout concepts and their rationale), `02-EVIDENCE-AND-CLAIMS.md` and `data/claims.json` |
| QA evidence | [`QA-REPORT.md`](QA-REPORT.md), [`qa/`](qa): `baseline-45b3296/` (before), `inventory-2026-10-27.md`, `review-en-2026-10-27.md`, `review-locales-2026-10-27.md`, `screenshots/` (after), test logs |
| Release and rollback | [`RELEASE-CHECKLIST.md`](RELEASE-CHECKLIST.md) |
| Static review copy | [`preview/`](preview), published by `.github/workflows/pages.yml` when committed |

## What changed in this revision

**Product truth.** Claim C05: SmartphoneKey does not support third-party card-programming devices (owner-stated, 27 October 2026; not a new hardware test). Public sentence: "Supported SmartphoneKey reader configurations also let you program MIFARE Classic and MIFARE DESFire EV3 cards." The technical answer "SmartphoneKey does not support third-party card programmers" appears once, on the compatibility page and in the MIFARE guide. Every page, table, FAQ, setup rule, metadata string and translation that implied a compatible programmer or a built-in programmer "where available" was rewritten. Card programming moved from the reader proposition to "additional capabilities" on the home, platform and readers pages. C13/C14 (reader Thread roles, shared uplink) are recorded as published in every claim document, matching the register.

**Editorial.** English rewritten from the deck (revision 2.1, corrections in 2.2): category "access management platform"; home H1 "Manage access across your properties in one place"; everyday tasks, ways to enter (Wallet keys, NFC cards, visitor QR code; the app is where keys are managed), events and status, readers with a built-in access controller, additional capabilities, audience paths, next steps. "Find your setup" became "Site recommendations" with the result fields Your selection / Recommendation / Why / Still to check on site / Guides for your selection / Discuss these recommendations. Demo disclaimers, filler introductions, "Entity" (except once), "credentials" as a blanket word, "lifecycle", "workflow" and "v2" wording are gone. The brand line stays in the footer only.

**Design.** Concept B of two measured layout hypotheses (`docs/site-v2/concepts/`): cool near-white base, one teal for actions and evidence, Manrope (SIL OFL, self-hosted, Latin and Cyrillic), 51–54 px desktop H1 and 34 px mobile H1, 17 px body, header with an existing-user row, product panel with the real reader image in the hero, system strip, task sequence, comparison cells, labelled workflow illustration on the platform page, inner-page openings with evidence and an action, recommendation result card, quieter footer. The warm paper theme, the 93–96 px slogan, the hero questionnaire and the dark automation band are gone. Mobile menu: action and existing-user links first, full-height sheet.

**Assets.** The only real product images are the installation guide's reader and exit-button images (from the `smartphonekey` module in spk-odoo), converted to transparent WebP cutouts. No Admin Panel or mobile app screenshot exists anywhere (inventory, section 3); the mobile walkthrough PNGs in spk-odoo are pre-release design mock-ups. The platform page uses a labelled illustration instead.

**Localisation.** The `.pot` was re-exported from the implemented templates; each catalogue (fr, de, es, uk) was rewritten by a dedicated worker from the frozen deck and glossary (841 public terms per language; the English-only legal pages, archived articles and biographies stay untranslated with a note in the page language). Checks: `tools/i18n_check.py` (coverage, placeholders, tags, forbidden wording, programmer wording) and an independent agent review of the rendered pages. No human native-speaker review has taken place; that remains an owner task before launch.

**Data records on existing databases.** The claim register, compatibility rows and guides are `noupdate` records. `migrations/18.0.3.0.0/post-migrate.py` reloads the three data files on upgrade and republishes the two card rows, overwriting editor changes to those records (stated in the changelog). A fresh install needs nothing.

## Integration decision (unchanged)

`spk_website_v2` depends on and extends the AP-428/AP-429 baseline (`spk_website`): `/` keeps the homepage switch, the baseline's Webflow URLs are retained or redirected, `/adminpanel`, `/referral-program` and the instruction site stay with their modules, and `spk_website_v2.enabled = False` hands every URL back to the baseline. To ship, copy the addon into spk-odoo, add it to the deployment and follow that repository's PR rules.

## Fallbacks in effect

* No range report: no distance anywhere.
* Matter controller role: "confirmed for each project".
* Shared uplink: published with its limits; the Matter guide topology is an example.
* AI Concierge v2: availability enquiry only.
* Certifications: document links with what each states; no badges.
* No booking URL configured: no booking link.
* No genuine Admin Panel screens: labelled illustration and tables.
* Marketing consent not implemented: no opt-in checkbox, no analytics loader.
* Instruction site not installable locally (Enterprise dependency of `smartphonekey`): the Instructions links were verified as links only; they return 404 on the local instance and must be checked on stage.

## Open items (owner role)

1. Marketing: a human native-speaker read of French, German, Spanish and Ukrainian (agent-reviewed only); a reviewed translation of the legal pages if they should not stay English.
2. Product owner / hardware: which reader configurations support card programming (the site says "supported reader configurations"); Matter controller role per reader (C13 covers Thread only); uplink loss behaviour (C14); range report (C15); FCC and ISED record check (C20); whether the exit button is supplied with the reader (the site says "a separate unit; check the package contents").
3. Product: approved Admin Panel and mobile app screenshots with demo data, to replace the illustration; AI Concierge v2 release status (C17); the ChatGPT app description; the referral programme (keep or retire).
4. Marketing: archived article review (they predate the register); current team roles; analytics loader and consent decision.
5. Operations: who receives website leads (website sales team and salesperson in Website settings).
6. Engineering: merge into spk-odoo, run its gates and `make test` on Odoo.sh, verify on stage (instruction routes 200, hreflang set with preview mode off, fonts served), then the release checklist.
