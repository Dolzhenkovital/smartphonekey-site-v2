# QA report: SmartphoneKey website 2.0, revision of 27 October 2026

> **Later update:** the homepage update of 30 October 2026 (real Admin Panel screenshots, Claude Design, claim C21) has its own report with its own evidence: [`qa/homepage-update-2026-10-30.md`](qa/homepage-update-2026-10-30.md). The measurements below describe the 27 October revision.

Environment checked: a **local Odoo 18 test instance** in Docker (`odoo:18.0`, build 18.0-20260409, PostgreSQL 16) with `spk_website_v2` 18.0.3.0.0 installed fresh on the AP-429 `spk_website` baseline, synthetic data only, `spk_website_v2.preview_mode=True` (40 px banner on every capture), plus the static review copy exported from it. **Production, the Odoo.sh stage and smartphonekey.com were not changed.** The regenerated `preview/` folder was committed (d48be4d) and, on the owner's instruction, pushed; the GitHub Pages workflow published it as the noindex review copy. "Pass" means passed in that local environment.

Evidence: `qa/odoo-tests.txt` (48 tests), `qa/lint.txt`, `qa/i18n-check-<lang>.txt`, `qa/static-export.txt`, `qa/screenshots/` (131 captures with `capture-log.txt` / `capture-log.json`), `qa/baseline-45b3296/` (the previous version, with measurements), `qa/inventory-2026-10-27.md`, `qa/review-en-2026-10-27.md` (independent English review, 41 findings), `qa/review-locales-2026-10-27.md` (independent review of the four translations), `qa/stage3a/`, `qa/stage3b/`, `qa/stage4-locales/` (interim captures).

## What this revision answers

The owner's assessment was that the site "looks different but not better", with awkward Ukrainian, an English source that read like internal notes, the wrong product priorities (card programming overstated, implying third-party programmers) and a layout that gave the first screen to a slogan and a questionnaire. This revision corrects claim C05, rewrites the English source and all four translations, and rebuilds the design from two measured concepts. Details: `IMPLEMENTATION-STATUS.md`; decisions: `../docs/site-v2/DESIGN.md`, `04-COPY-DECK-EN.md`; execution ledger: `../docs/site-v2/CLAUDE-MASTER-BRIEF-EN.md`.

## Gates run

| Gate | Command | Result |
|---|---|---|
| Odoo tests, fresh test database with the final catalogues | `docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d spk_v2_test --db-filter='^spk_v2_test$' -u spk_website_v2 --i18n-overwrite --test-enable --test-tags /spk_website_v2 --stop-after-init` | **48 tests, 0 failed, 0 errors** (`qa/odoo-tests.txt`). New: `test_setup_result.py` (result fields without JavaScript, empty state, contact prefill note, home-tool `site` mapping, label order) |
| Translation checks | `python tools/i18n_check.py --addon addons/spk_website_v2 --lang <uk|fr|de|es> --verbose` | 846 public terms translated in each language; **blocking 0** in all four; warnings uk 14, fr 13, de 12, es 12, all intended (product names, FCC/IC identifiers, the title template) |
| Soft hyphens | `python tools/i18n_soft_hyphens.py --addon addons/spk_website_v2` | Paragraph text only (terms ≥ 80 characters, words ≥ 16): de 64, es 6, fr 3, uk 6 terms touched; headings untouched |
| pylint-odoo (`--disable=all --enable=odoolint --fail-under=9.0`, in a `python:3.12-slim` container) | see `qa/lint.txt` | **9.99/10**, passes; the only notice is the OCA author template, as before |
| OCA `oca-checks-odoo-module` (current hook version) | `qa/lint.txt` | Style notices only: XML header casing (`utf-8` vs `UTF-8`) and attribute order (`id` before `class`) in `resources.xml`, `setup.xml`, `solutions.xml`; not fixed, no functional effect |
| Static review copy | `MSYS_NO_PATHCONV=1 python tools/export_static.py --odoo http://127.0.0.1:8069 --out preview --base /smartphonekey-site-v2 --external https://spkey.odoo.com` then `python tools/check_static.py preview --base /smartphonekey-site-v2` | 190 pages, 10 redirects, 35 assets (now including the four Manrope subsets referenced from the CSS bundle); **no problems** |
| Screenshot matrix | `node tools/capture_screens.mjs http://127.0.0.1:8069 qa/screenshots` | 131 captures: the five core pages (home, platform, readers, setup result, contact) at 1440×900 and 390×844 in all five languages, English at the eight sizes, German and Ukrainian at 320/768/1024/1280/1920, no-JS, reduced motion, 200 % zoom, menus, errors, long tables, guides, 404. **0 elements outside the viewport in every capture; Manrope loaded in every capture** |
| Module upgrade of an existing database | `-u spk_website_v2` on the previous 18.0.2.1.0 database | Migration `18.0.3.0.0/post-migrate.py` reloaded the three content data files and republished the two card rows (logged); SCSS compiled with 0 warnings |
| Hallmark sloplint | not run | The brief withdrew the linter's per-screen word budget as a gate; the earlier D1 deviation no longer applies |
| Lighthouse / Core Web Vitals | not run | No lab runner in the environment; size budgets below |

## Before and after, same sizes (preview banner present in both)

| Measure | Before (45b3296) | After |
|---|---|---|
| Home H1 size / lines, 1280×800, English | 92.8 px / 3 | 50.9 px / 2 |
| Home H1, 1280×800, Ukrainian | 92.8 px / 4 | 50.9 px / 2 |
| Home H1, 390×844, Ukrainian | 44 px / 3 | 34 px / 3 (4 at 320 px) |
| First primary action bottom, home 1280×800 | 755 px (uk), 661 px (en) top edge, questionnaire beside it | 563 px (en, uk), 584 px (de); the three-cell system explanation ends at 768 px |
| First primary action on the readers page, 1280×800 | 5 204 px (closing section) | 648 px (in the opening, beside the product photo) |
| First primary action on the platform page, 1280×800 | 5 012 px | 614 px (opening with the labelled workflow illustration) |
| Product evidence on the home first screen | none (photo in section 4, lazy) | real reader image in the hero panel, eager; three-part system strip |
| Card programming | second sentence of the reader section, "compatible programming device" | "additional capabilities" rows; no programmer wording anywhere (tested in English, checked in the four catalogues) |
| Home page height at 390 px | 6 231 px (uk) | 8 484 px (uk), 7 796 px (en): more content (tasks, ways to enter, status, capabilities, audience paths, the compact tool at the end) |
| Typeface | General Sans (no Cyrillic; system sans on /uk) from a third-party CDN | Manrope, self-hosted, one face for all five languages |
| Translation checks | uk 5 blocking (programmer wording), es 9, fr 1, de 1 | 0 blocking in all four |

## Acceptance matrix (07-DELIVERY-AND-ACCEPTANCE, plus the brief of 27 October)

| ID | Result | Evidence |
|---|---|---|
| A01 First screen | Pass | `en-home-1280x800.jpg`, `uk-home-390x844.jpg`: category line, H1, lead, filled action, real reader image, Admin Panel → ways to enter → reader strip. The independent reviewer identified the product, audience and next action from the first screen (agent check, not a user study: `review-en-2026-10-27.md` §1) |
| A02 Independent journeys | Pass | Explore, site recommendations (result without contact details, inputs shown as chips, recommendation with reason, site checks, guides, contextual contact link), compatibility, guides, partner; no demo gate, demo disclaimers removed |
| A03 JavaScript off | Pass | `test_result_has_every_field_without_javascript`, `test_setup_result_without_javascript`, `test_without_javascript`; `en-setup-no-js-390.jpg`, `en-contact-no-js-1440.jpg`, `en-readers-no-js-1440.jpg`; menus are `<details>` |
| A04 Routes, titles, H1 | Pass | `test_required_routes_are_substantive_and_unique`; titles ≤ 65 characters and descriptions ≤ 160 in the four catalogues (locale review §6; one German description at 162) |
| A05 Card names | Pass | Only MIFARE Classic and MIFARE DESFire EV3; `test_claim_scope_on_the_new_pages` rejects EV1/EV2 and sizes; `i18n_check.py` rejects programmer wording in every language |
| A06 Matter / network | Pass | Roles distinguished; Thread roles published per the owner; Matter controller "confirmed for each project"; one hub per scenario; no range figure, no failover promise |
| A07 Concierge | Pass | Availability-enquiry wording (tested sentence kept) |
| A08 Accepted vs opened | Pass | Offline guide states and the tested sentences; the home status section and the platform workflow illustration show pending vs confirmed |
| A09–A12 Enquiry persistence, retries, hostile input, failure keeps values | Pass (local) | `test_enquiry.py` unchanged in substance; contact form re-ordered (project details first) and the prefill note added; preview mode still never sends |
| A13 Keyboard, labels, 200 %, 320 px | Pass | Independent review §5: one h1, skip link, labelled inputs, visible focus on every control, focused error summary linked to fields, Enter/Escape on menus, 200 % reflow without horizontal scroll, text contrast ≥ 5.39:1; `en-platform-zoom-200.jpg`, `en-contact-zoom-200.jpg`, `en-contact-errors-1440.jpg`; 0 overflow at 320 and 390 in all languages. No screen-reader session was run |
| A14 Reduced motion | Pass | No transitions or animations; `en-home-reduced-motion-1440.jpg` |
| A15 Portal and guides unaffected | Pass (local) | `test_marketing_assets_stay_off_the_login_page`; every rule scoped under `html.spk-site-v2`; the instruction site itself is not installable locally |
| A16, A17 Old URLs, real 404 | Pass | `test_every_snapshot_url_has_its_intended_answer`, `test_unknown_route_is_a_real_404`; the 404 now carries no canonical, breadcrumb or JSON-LD |
| A18 Structured data | Pass | `test_structured_data_matches_the_page`; no FAQPage, Product, Offer, rating |
| A19 Sitemap and robots | Pass (local) | `test_sitemap_lists_published_canonical_pages_only`, `test_robots_keeps_search_and_training_decisions_separate`, `test_preview_is_never_indexed` |
| A20 Public deployment | **Not done** | Nothing deployed; the preview folder is regenerated locally only |
| A21 Analytics | Unchanged | Enum-only events into an existing `dataLayer`; no loader, no consent (release decision) |
| A22 Editor updates a row | Pass | `test_editing_a_published_row_sends_it_back_to_review` (label now "Product facts checked") |
| A23 Performance | Budgets met by size | Static copy: CSS 47.5 KB (7.9 KB gzip, budget 80), scripts 2.7 + 1.1 + 2.2 KB gzip, home HTML 6.6 KB gzip (uk 8.1 KB), largest image 38.9 KB (reader cutout), fonts 57 KB in four subsets loaded by unicode-range (new cost; the previous version loaded General Sans from Fontshare, not counted). Lab score and field Core Web Vitals not measured |
| Brief §10 Content | Pass | No third-party programmer implication in active content, data, metadata or translations; card programming secondary; five languages agent-reviewed independently (`review-locales-2026-10-27.md`), Should-fix items applied, remaining items listed below |
| Brief §10 Design | Pass with notes | At 1280×800 and 1440×900 the category, benefit, action and product evidence are visible; on phones the action precedes any form; longest translations hold on two desktop lines; no clipped words, no tiny text, soft hyphens only in paragraph words ≥ 16 characters. Notes: the home H1 takes four lines at 320 and 375 px; the phone home page is long (see remaining items) |
| Brief §10 Functional | Pass (local) | Setup combinations tested (Wi-Fi, cellular, both, not sure; home tool mapping); locale and context preserved into `/contact` (`test_setup_guide_and_enquiry_speak_the_visitor_language`, `test_contact_prefill_note_follows_the_recommendations`); no real enquiry sent |

## Review findings and their status

Independent English review (`review-en-2026-10-27.md`, 0 blocking, 11 should-fix, 30 minor): the eleven should-fix items are resolved (entry claims F3/F11, category on the first screen F1, platform and inner openings F4/F25, home tool mapping F22, exit button F12, mobile menu F7, phone home length F5 partly, date and canonical F39, terminology F13–F15), except F38 and F41, which need a staging environment (hreflang with preview mode off; instruction routes served by `smartphonekey`). Minor items applied: F6, F9, F24, F26–F29, F31–F34, F36, F37. Not applied: F8 (65ch paragraph width retained by design), F35 (chip border contrast, decorative), F23 (`interest=technical` maps to "Product compatibility"; no technical enquiry type exists).

Independent locale review (`review-locales-2026-10-27.md`): the "stale database" blocking item was the review instance, not the catalogues, and is gone with the fresh install (checked: `/uk/compatibility` shows the new rows and "Дані про продукт перевірено 27 жовтня 2026 р."). All Should-fix items were applied by the locale workers (Ukrainian 4, French 7, German 5, Spanish 10) together with most Minor items; declined ones are listed in the ledger. The date format finding (X2) is fixed in `rendering.py` (long format per locale: "27. Oktober 2026", "27 de octubre de 2026", "27 жовтня 2026 р.").

## Deviations and limitations

* **D1. No human native-speaker review.** The four translations were written and then independently reviewed by agents against the glossary and the rendered pages. The owner should have each language read by a person before launch.
* **D2. Instruction site.** `/guide-for-usage-and-installation` and `/instructions/*` return 404 on the local instance because the `smartphonekey` module cannot be installed here; the links are correct for the stage and production hosts (the static copy points them at spkey.odoo.com).
* **D3. hreflang.** Alternates are omitted in preview mode by design, so the 5 + x-default set was verified by test (`test_pages_render_in_each_language`) and not in the review copy.
* **D4. Phone home page length.** 7 800–8 500 px at 390 px (the reviewer suggested about 6 500 px); the content is the eight sections the brief asks for, each short; the primary action sits at 538–565 px.
* **D5. H1 at 320 and 375 px** wraps to four lines in English, German and Ukrainian (three at 390 px).
* **D6. OCA style notices** (XML header casing, attribute order) left as reported.
* **D7. Lab performance** not measured (no Lighthouse runner); size budgets met.
* **D8. Exit button supply status** unknown: the caption says "a separate unit; check the package contents and your door's hardware in the guide".

## Static review copy

`preview/` was regenerated from the fresh local instance (190 pages in five languages, redirects as noindex refresh pages, fonts and images copied, `Disallow: /`, banner and `noindex` on every page, contact form never sends). It was committed as d48be4d and published by the `Publish test preview` workflow (run 40557310033) on the owner's instruction. Live check on 27 October 2026: home, `/uk/`, `/de/products/readers/`, `/fr/find-your-setup/`, `/es/compatibility/`, the Manrope files, the reader image and the CSS answer 200; an unknown URL answers 404; every page carries `noindex, nofollow` and the banner; the new English, Ukrainian and Spanish strings are present and no programmer wording remains.
