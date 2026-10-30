# Homepage update of 30 October 2026: execution report

Brief: `../docs/site-v2/CLAUDE-HOMEPAGE-UPDATE-2026-10-30.md`. Base: repository `smartphonekey-site-v2` at commit 6d2b1e6 (main), working tree with 30 pre-existing modified JPEGs in `qa/baseline-45b3296/` (left untouched). Result: **ready for review; the static review copy is published on GitHub Pages** (owner's instruction of 30 October 2026, "push and deploy to GitHub Pages"). Commit eed3919 on `main`, pushed; Pages run [41125397562](https://github.com/Dolzhenkovital/smartphonekey-site-v2/actions/runs/41125397562) succeeded. Odoo stage and production, DNS and smartphonekey.com were not changed; no enquiry, message, key or door action was performed.

Environment checked: the local Odoo 18 test instance in Docker (`odoo:18.0`, PostgreSQL 16, `spk_website_v2` updated to 18.0.4.0.0 on the AP-429 `spk_website` baseline, `spk_website_v2.preview_mode=True`, synthetic data only) and the static review copy regenerated from it into `preview/`. "Pass" means passed in that environment.

## 1. Scope and revision

A substantial homepage rewrite and recomposition around seven real Admin Panel screenshots, with targeted changes to `/platform`, `/platform/access-management`, `/products/readers` and `/platform/visitor-access`. Addon version 18.0.3.0.0 → 18.0.4.0.0 (`CHANGELOG.md` 4.0.0). Copy deck revision 3.0 (`../docs/site-v2/04-COPY-DECK-EN.md`, home section rewritten, change notes under the three supporting pages); design contract revised (`../docs/site-v2/DESIGN.md`, "Revision of 30 October 2026").

## 2. Claude Design

Used as required: the Design canvas inside Claude (standalone claude.ai/design is being retired; the Design artifact type is its current form). Canvas: **https://claude.ai/artifact/9oC9RXTa2CPdVVY2KTPwZ3** ("SmartphoneKey homepage 2026-10-30", version 3). Artboard sources, `canvas.json`, exported previews and the decision: `../docs/site-v2/design/2026-10-30/` (README, `artboards/`, `previews/`).

| Artboard | Designed there |
|---|---|
| Opening A | Platform screen with a smaller reader: copy 8/12, compact reader card 4/12, full Dashboard beneath |
| Opening B | Balanced screen and reader with a Wallet statement: copy 6/12, one panel with the Dashboard close-up and the reader |
| Main (1280) | The selected direction A through the whole page: hero, benefits, journey, situations, AI Assistant, reader and connection example, capabilities, closing |
| Mobile (390) | The same page at phone width |
| Platform (1280) | The affected platform opening and monitoring section |

**Selected: A.** The real panel is recognisable at about 56 % of its captured width across the container (measured in the implementation: 1167 px of 2133 at a 1280 px viewport), against about 45 % for B's close-up tile; the 8/12 copy column keeps every language's H1 on two lines at 1280 px (B's 6/12 column does not for German); one dominant software image and a modest hardware image, as the brief asks; on phones the order copy, actions, reader card, Dashboard close-up puts the product evidence directly after the actions; B's Wallet strip repeats benefit 2. Both openings used the same facts, actions and assets.

Export limitations: the canvas has no image export of its own in the version used; the previews are Chrome screenshots of the canvas and its focused views (the phone artboard is a fluid page and renders at window width in the focused view, so its phone rendering is documented through the implementation captures). The built-in browser of the desktop app is not signed in to claude.ai; the owner's Chrome was used to view and capture the canvas.

## 3. Changed files

Addon: `views/home.xml` (rewritten), `views/platform.xml` (platform and access-management openings and sections, visitor-access sentence), `views/products.xml` (Thread section), `views/components.xml` (`connection_example`), `static/src/scss/site.scss` (hero reader card, Dashboard figure, benefits, journey, split evidence, connection example, capabilities, expanded view), `static/src/js/expand.js` (new), `static/src/img/product-ui/` (18 WebP derivatives, 456 KB), `site_content.py` (dates, home description, note on the kept `HOME_*` strings), `controllers/main.py` (home no longer serialises the setup rules), `data/website_claims.xml` (C21), `i18n/*.pot|po` (93 new public strings), `tests/test_routes.py` (new screenshot test, updated server-rendered phrases), `tests/test_seo.py` (forbidden wording extended), `__manifest__.py`, `CHANGELOG.md`. Tools: `tools/product_ui_images.py` (new), `tools/i18n_apply.py` (new), `tools/capture_screens.mjs` (lazy images loaded before full-page captures). Registers and docs: `registers/claims.md`, `IMPLEMENTATION-STATUS.md`, `README.md`, `QA-REPORT.md` (pointer), `../docs/site-v2/02-EVIDENCE-AND-CLAIMS.md`, `data/claims.json`, `04-COPY-DECK-EN.md`, `DESIGN.md`, `00-START-HERE.md`, `design/2026-10-30/`. Static copy: `preview/` regenerated.

## 4. Copy and claim decisions

- English copy follows the brief's blocks 1–8; visible words on the home page: 638 (brief target 550–750). Adopted from the colleague: concrete benefits, visible Wallet messaging, installation → grant → enter, four everyday situations, reader/controller and Thread explained beneath the benefit, a real AI Assistant section. Rejected: property-management positioning, the repeated "everything works together" sections, "Revoke access instantly", "Just ask. SmartphoneKey handles the rest.", Matter over Thread as a headline, "wireless" without conditions, quantified savings, duplicate camera lists.
- New claim **C21 Admin Panel AI Assistant**: evidence "UI-observed 2026-10-30" stored as `code_supported` (the model's enum has no UI-observed value; the observation and its limits are in the record), publication `public_scoped`, allowed sentence "Get help in the Admin Panel with the built-in AI Assistant. Available actions depend on your permissions and site configuration." Recorded in `data/website_claims.xml`, `data/claims.json`, `registers/claims.md`, `02-EVIDENCE-AND-CLAIMS.md`. AI Assistant, the SmartphoneKey app in ChatGPT and AI Concierge (C17, still availability enquiry) are kept separate on the home, access-management, visitor-access and apps pages.
- Offline qualification kept near the "Someone leaves" scenario ("Changes for an offline reader remain pending until it reconnects and applies them") and in full on the platform and access-management pages. Infrastructure conditions kept beside the benefit line. Card programming stays an additional capability (C05). No range, node count or failover promise (the readers page states "automatic failover is not implied").
- The compact recommendations tool left the home page; `/find-your-setup` keeps the `site` parameter and the `HOME_*` strings.
- `test_seo.FORBIDDEN` now also rejects instant revocation, "handles the rest"/"Just ask.", and "access in seconds"/"less training"/"faster management" on every public page.

## 5. Image placements

| File (derivatives in `static/src/img/product-ui/`) | Where it renders | Note |
|---|---|---|
| `01-admin-dashboard.jpg` → `admin-dashboard-{800,1200,1600,2133}.webp`, close-up `admin-dashboard-close-up-936.webp` | Home hero (eager, `fetchpriority="high"`; the close-up through `<picture>` on ≤ 640 px); expanded view opens the 2133 px file. Close-up also in the `/platform` opening with "View the full Dashboard" | Caption says English interface and that the figures are interface values of a test account |
| `02-ai-assistant-detail.jpg` → `ai-assistant-detail-422.webp` | Home "Help inside the Admin Panel"; `/platform/access-management` assistant section | Natural width 422 px, never stretched |
| `02-ai-assistant.jpg` → `ai-assistant-context-{1200,1600,2370}.webp` | `/platform/access-management`, "See it beside the Dashboard" (expanded view) | Context only; the detail is the visible image |
| `03-assign-access.jpg` → `assign-access-dialog-548.webp`, `assign-access-1056.webp` | Home journey step "Grant access"; `/platform/access-management` opening with "View the full screen" | Complete dialog with a 24 px margin; caption: step 2 of 3 before a person is chosen |
| `04-device-status.jpg` → `device-status-close-up-1404.webp`, `device-status-{1200,2133}.webp` | `/platform`, "Know when a change has reached the door" | Caption: interface evidence of monitoring, not a network layout |
| `05-recent-activity.jpg` → `recent-activity-close-up-620.webp`, `recent-activity-967.webp` | Home situations; `/platform/access-management` events section | Caption: a record, not proof that a person passed through |
| `06-guest-wallet-key.jpg` → `guest-wallet-key-dialog-548.webp`, `guest-wallet-key-1304.webp` | Home situations; `/platform/access-management` contractor example with "View the full screen" | Complete dialog; caption: shown before anything is sent, dates are form defaults |

Omitted: nothing from the package. The readers page shows no screenshot (the Devices filters are monitoring evidence, placed on the platform page as the brief allows). No synthetic UI anywhere: the "ways to enter" tile and the connection layout are labelled lists. Every derivative was reopened and inspected after conversion (dashboard close-up widened to 936 px so the Give Access button is complete; dialogs complete; no QR codes, contacts or credentials). `test_product_screenshots_are_served_and_described` checks that every product image on the four pages is served, has alt text and dimensions, that the expand links resolve, and that only the Dashboard is eager.

## 6. Language review

English is the source. The `.pot` was re-exported from the updated database; `tools/i18n_build.py` reported 92 (then 1 more) untranslated public terms per language, all translated (`translations-2026-10-30.json`, applied with `tools/i18n_apply.py`), `tools/i18n_check.py`: blocking 0 in uk/fr/de/es (warnings are the known product-name and placeholder notices), `tools/i18n_soft_hyphens.py` run, catalogues reloaded with `-u spk_website_v2 --i18n-overwrite`. Product screenshots stay English in every language; captions and alt text are translated and name the English interface where the English caption does.

Independent reviews by one agent per language (reports `review-uk.md`, `review-fr.md`, `review-de.md`, `review-es.md`): see the table below for counts and what was applied. No human native-speaker read has taken place (unchanged owner item).

| Language | Reviewed | Blocking | Should-fix | Minor | Applied |
|---|---|---|---|---|---|
| Ukrainian | 93 | 0 | 6 | 12 | all 18 (`translations-fixes-uk.json`): "still" misread, entrance/site-team terms, two caption calques, the AI Concierge sentence, the status sentence; minor consistency items |
| French | 93 | 0 | 11 | 6 | all 17 (`translations-fixes-fr.json`): non-breaking spaces before : ; ? in the 11 new strings, délivrer / titulaire de clé / pris en charge / dispositif de verrouillage / lorsque, four awkward sentences, the shorter home H2 |
| German | 93 | 0 | 14 | 9 | all 23 (`translations-fixes-de.json`): Zutrittsmanagement, Mitarbeitende, Team vor Ort, entziehen / ausstellen / übernehmen, the status paragraph, "Anzeigewerte", the Devices and Guest Key captions, minor idiom and word-order items |
| Spanish | 93 | 0 | 10 | 8 | all 18 (`translations-fixes-es.json`): "Llega un nuevo residente", "cuando se admita", the status sentence, the Devices caption, "in situ", "Dashboard del Admin Panel", "llave en Wallet", "Cómo colaborar", the shorter home H2, "Emita"; lowercase "internet" and the other consistency items |

After the fixes every catalogue passes `i18n_check.py` with blocking 0; the corrected catalogues were reloaded into the serving database and the final test run, static copy and screenshot matrix were produced from them. Observations the reviewers made outside the batch, not changed: the French home shows two existing renderings of "Connected-device scenarios" ("Scénarios d'appareils connectés" in the capabilities list, "Scénarios pour appareils connectés" in the link); "An employee needs another door" is rendered with "employee" rather than the glossary's "staff" because the English source says employee.

## 7. Tests and checks actually run

| Check | Result |
|---|---|
| Odoo tests, fresh update of the test database with the final catalogues: `docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d spk_v2_test --db-filter='^spk_v2_test$' -u spk_website_v2 --i18n-overwrite --test-enable --test-tags /spk_website_v2 --stop-after-init` | **49 tests, 0 failed, 0 errors** (`qa/homepage-update-2026-10-30/odoo-tests.txt`); the earlier subset run caught one wrong threshold in the new test, fixed |
| Module update of the serving database (`-u spk_website_v2`) | C21 created from the `noupdate` file (verified in `spk_website_claim`), SCSS compiled, no errors (`i18n-reload.txt`) |
| Translation checks (`i18n_check.py`, four languages) | blocking 0 each (uk 15, fr 14, de 13, es 13 warnings, all known) |
| Screenshot matrix (`node tools/capture_screens.mjs`, five languages, eight desktop/phone sizes, no-JS, reduced motion, 200 % zoom, menus, errors; 131 captures) | `screenshots/capture-log.txt`: 0 capture errors, 0 elements outside the viewport in every capture, Manrope reported loaded in 130 of 131 captures (the 320 px English home ran its font check before the face settled; the 390 px capture of the same page reports it loaded); H1 two lines at 1280/1440 in all five languages, three at 390 (four at 320); first primary action at y = 506–554 (en) / 536–584 (de, uk) at 1280×800; the Dashboard is on the first screen at 1280×800 and 1440×900. The capture tool now walks each page before a full-page capture so the lazy product screenshots are in the image (with the mouse wheel when JavaScript is off) |
| Expanded view in the browser (home, 1280 px) | "View larger" opens the dialog with the 2133 px image, focus on Close; close returns focus to the link; 0 overflowing elements; Dashboard rendered at 1167 × 492 px (55 %) |
| Static review copy (`tools/export_static.py` + `tools/check_static.py`) | 215 pages and 262 URLs checked, **no problems**; the copy carries the product images, `expand.js` and the new metadata |
| Lint (pylint-odoo, OCA checks) | not re-run in this update (no Python model or security change; `controllers/main.py` and `site_content.py` edits are one-line) |
| Lighthouse / field Core Web Vitals | not run (no lab runner); size budget: product images 456 KB in total, the hero loads one of 800/1200/1600/2133 px by viewport (13–51 KB), CSS bundle 56 KB uncompressed |
| Hallmark sloplint | not run (per-screen word budget withdrawn on 27 October) |
| Instruction site, hreflang with preview mode off, production deployment | not checkable locally (unchanged D2/D3/A20 of the 27 October report) |

## 8. Before and after (same sizes, preview banner present)

| Measure | Before (6d2b1e6) | After |
|---|---|---|
| Home H1 lines, 1280×800, en / de / uk | 2 / 2 / 2 | 2 / 2 / 2 |
| First primary action bottom, home 1280×800, en / de / uk | 563 / 584 / 563 px | 554 / 584 / 584 px |
| Product evidence on the first desktop screen | reader cutout, three-cell strip | reader card and the real Admin Panel Dashboard (top of the capture visible at 800 px height) |
| Real Admin Panel screenshots on the site | 0 | 7 subjects, 6 pages/blocks |
| Home page height at 390 px, en / de / uk | 7 796 / 8 583 / 8 484 px | 9 584 / 10 008 / 10 008 px (five captioned screenshots) |
| Home page height at 1280 px, en / de / uk | 4 762 / 5 057 / 5 010 px | 5 825 / 6 073 / 6 113 px |
| Visible English words on the home page | about 560 | 638 |

Before captures: `before/` (27 October captures of the affected pages). After: `screenshots/`.

## 9. Unresolved gaps and limits

- No real iPhone/Android Wallet screen, native app screen, successful AI conversation, Scenario Builder or camera capture exists; the "Enter" step uses a labelled list, and the AI section shows only the unedited greeting. Stronger assistant copy needs an implementation contract and release evidence (C21 limits).
- Translations are agent-written and agent-reviewed; a human native-speaker read remains an owner task.
- The phone home page is long (9.6–10 kpx) because of five captioned screenshots; each is complete and legible at 390 px. A shorter phone variant would mean dropping evidence the brief asks for.
- The static copy points instruction links at spkey.odoo.com; the instruction site is not installable locally.
- Publication status: the review copy at https://dolzhenkovital.github.io/smartphonekey-site-v2/ shows this update (noindex, preview banner, form never sends). Checked after deployment: home in en/fr/de/es/uk, `/platform`, `/platform/access-management`, `/products/readers` and `/uk/platform/access-management` answer 200 with the expected H1; all eight product-image files and `expand.js` answer 200; the hero image loads, Manrope loads, the expanded view opens; no console errors. This is a review site, not an Odoo deployment: merging into spk-odoo and the stage/production checks remain the engineering items of `IMPLEMENTATION-STATUS.md`.
- Deployment incident: the push-triggered run 41124486087 failed in `deploy-pages` ("Fetching artifact metadata failed", a transient GitHub error; the log download also returned "Egress is over the account limit"). Re-running its failed job failed again because the run then held two `github-pages` artifacts. A fresh `workflow_dispatch` run (41125397562) on the same commit deployed successfully. The 30 pre-existing modified JPEGs in `qa/baseline-45b3296/` were left uncommitted.
