# QA report: SmartphoneKey website 2.0

Date: 27 October 2026. Environment checked: a **local Odoo 18 test instance** in Docker (`odoo:18.0`, build 18.0-20260409, PostgreSQL 16) with `spk_website_v2` installed on the AP-429 `spk_website` baseline and synthetic data only, plus the static review copy built from it. **Production, the Odoo.sh stage and smartphonekey.com were not changed or checked as deployments.** "Pass" below means passed in that local environment.

Evidence files are in [`qa/`](qa/): `odoo-tests.txt`, `concurrency.txt`, `hallmark-sloplint.txt`, `robots-production-mode.txt`, `sitemap-production-mode.xml`, `legacy-routes.txt` and 57 screenshots in `qa/screenshots/` (English at eight sizes plus JavaScript off, reduced motion and 200% zoom; French, German, Spanish and Ukrainian home, readers and resources pages, and the language menu).

**Update of 27 October 2026.** Re-run after three owner instructions: every reader can act as a Thread Border Router and mesh router (claim C13 published, see `registers/claims.md`); the site is in English, French, German, Spanish and Ukrainian; certificates and the existing instruction page are linked prominently (header "Instructions" link to `/guide-for-usage-and-installation`, Certifications in the main menu, an Instructions section on Resources and an Instructions column in the footer). The instruction page itself is unchanged.

## Gates run

| Gate | Result |
|---|---|
| Odoo tests (`--test-tags /spk_website_v2`, fresh database, five languages) | **42 tests, 0 failed, 0 errors** (`qa/odoo-tests.txt`) |
| Translation coverage (`test_every_site_string_is_translated`, `tools/i18n_build.py`) | French, German, Spanish, Ukrainian: every page term and every site string translated; placeholders identical |
| Layout in five languages (headless Chrome) | 270 page renders at 320–1440 px: nothing outside the viewport; desktop header on one row from 1201 to 1920 px in every language (Menu below); long German, Spanish, French and Ukrainian words break at soft hyphens |
| pylint-odoo (`--enable=odoolint --fail-under=9.0`, the spk-odoo recipe, in a Linux container) | **9.91/10**, passes. Remaining notices: OCA author and README template (not applicable to a company module; the baseline has the same) |
| OCA `oca-checks-odoo-module` | No findings |
| SCSS compilation (libsass 0.22, the version in the Odoo image) | Compiles; Odoo served the bundle with every style applied |
| Static review copy link check (`tools/check_static.py`) | 43 pages, every internal link and asset resolves, all noindex, canonicals on smartphonekey.com, no tokens or local addresses |
| Hallmark sloplint, render tier, 20 pages (`qa/hallmark-sloplint.txt`) | Home and About: 0 FAIL. 18 deep pages: FAIL 58 only (see deviation D1). REFLEX findings answered below. Re-run on the home page after the language and header changes: English 0 FAIL; German home 99 words on one lower screen (rule 58, translation length); the Ukrainian "CTA below 1280×800" finding comes from the preview banner (804 px with it, 764 px without) |
| spk-odoo changelog / guide-sync / i18n gates | **Not applicable here**: this module lives in its own repository and does not touch `smartphonekey`, its changelog, guides or portal strings. They apply when the module is merged into spk-odoo |
| spk-odoo `make test` on Odoo.sh | **Not run**: needs the private repository build |

## Acceptance matrix (07-DELIVERY-AND-ACCEPTANCE)

| ID | Result | Evidence |
|---|---|---|
| A01 First screen | Pass | `home-1440x900.jpg`, `home-390x844.jpg`, `home-1280x800.jpg`: H1, one sentence, "Explore the platform", the working setup tool; the reader appears only in section 4 |
| A02 Independent journeys | Pass | Explore (`/platform`), setup (`/find-your-setup`, result without contact fields), compatibility, guides, partner (`/contact?interest=partner`) each complete on their own; no popup, no booking gate. Browser-tested setup and contact prefill |
| A03 JavaScript off | Pass | `test_content_is_server_rendered`, `test_setup_result_without_javascript`, `test_without_javascript`; screenshots `setup-no-js-390.jpg`, `contact-no-js-1440.jpg`, `readers-no-js-1440.jpg`. Menus are `<details>` and work without script |
| A04 Routes, titles, H1 | Pass | `test_required_routes_are_substantive_and_unique`: every route 200, one H1, unique title and description, canonical, >60 words of body, no placeholder text. Each translated page: `lang`, translated H1, its own canonical, five `hreflang` alternates plus `x-default` (`test_pages_render_in_each_language`) |
| A05 Card names | Pass | Only MIFARE Classic and MIFARE DESFire EV3; `test_claim_scope_on_the_new_pages` rejects EV1/EV2 and memory sizes |
| A06 Matter / network | Pass | Roles distinguished (Matter guide table); every reader stated as Thread Border Router and mesh router per the owner's instruction, Matter controller role kept "confirmed for each project"; one-hub limit on home, automation, compatibility; no 80 m and no failover promise (tested); the distance row cannot be published (`test_rows_of_ungated_claims_cannot_be_published`) |
| A07 Concierge | Pass | Availability-enquiry wording only; no live door integration; tested phrase |
| A08 Accepted vs opened | Pass | Offline guide table and access-management copy; tested phrases |
| A09 Enquiry persists | Pass (local) | Browser submission created one lead with typed context; HTML stored escaped; `test_valid_enquiry_creates_one_lead_with_its_context`. Success is shown only after the server answers |
| A10 Retries and concurrency | Pass (local) | `test_retries_and_concurrent_duplicates_create_one_lead`, `test_insert_race_is_resolved_by_the_unique_index`; real run: 8 simultaneous identical POSTs gave 1 `created` + 7 `duplicate`, 1 lead (`qa/concurrency.txt`). One lead means one notification |
| A11 Hostile input | Pass | Missing CSRF 400; overlong 400 with field error; HTML escaped; `user_id`, `team_id`, `company_id`, `stage_id`, `email_to` ignored; honeypot rejected; throttle 429 after 5 in 10 minutes |
| A12 Failure keeps values | Pass | No-JS error re-render keeps every value and the submission ID; JS path keeps the form, shows the email fallback (`contact-errors-1440.jpg` shows the error summary). Network-interruption behaviour checked in code, not by cutting a live connection |
| A13 Keyboard, labels, 200%, 320 px | Pass | Skip link, visible focus, Enter opens menus, Escape closes and returns focus (browser-tested); labelled fields, `aria-invalid`/`aria-describedby`, focusable error summary; `platform-zoom-200.jpg`, `contact-zoom-200.jpg`; 0 elements outside the viewport on 26 pages at 320, 390, 768 and 1024 px. No screen-reader session was run |
| A14 Reduced motion | Pass | Only two 120 ms transforms on buttons, removed under `prefers-reduced-motion`; no autoplay; `home-reduced-motion-1440.jpg` |
| A15 Portal and guides unaffected | Pass (local) | The bundle loads only from the 2.0 layout; `test_marketing_assets_stay_off_the_login_page`; every rule is scoped under `html.spk-site-v2`. The instruction site could not be installed locally (Enterprise dependency of `smartphonekey`), so its pages were not rendered side by side |
| A16 Old URLs | Pass for the 34-URL snapshot | `registers/redirects.json`, `qa/legacy-routes.txt`, `test_every_snapshot_url_has_its_intended_answer`: 8 redirects end on a 200 page without chains. Live history (Search Console, backlinks, Webflow redirect settings) was not available |
| A17 Real 404 | Pass | Unknown URLs, unknown guides, posts and team slugs answer 404 in the 2.0 shell |
| A18 Structured data | Pass | One JSON-LD block per page; Organization and WebSite on home; BreadcrumbList matches the visible trail; Article on guides and posts with real dates; no Offer, Product, rating, address, SKU, price, SearchAction or FAQPage (tested by type and key) |
| A19 Sitemap and robots | Pass (local) | Sitemap lists every published canonical page in each language where it is translated (English-only pages once), plus the instruction routes when `smartphonekey` is installed; no redirects, noindex or referral page. Robots: one `User-agent: *` group with the private-route exclusions, tested for Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot, GPTBot and ClaudeBot; training crawlers are not singled out (the live robots.txt has no training rule, so that policy is preserved; any rule added in Website settings is appended). Preview and neutralized databases answer `Disallow: /` plus `noindex` and `X-Robots-Tag` |
| A20 Public deployment | **Not done** | No production or stage deployment was in scope. The GitHub Pages copy is a static review copy, not a deployment of the Odoo site |
| A21 Analytics | Pass with a gap | Events defined (`setup_completed`, `enquiry_submitted`, `booking_link_opened`) carry enums and paths only and fire only into an existing `dataLayer`. No analytics loader is included: consent handling for the actual jurisdiction is a release decision |
| A22 Editor updates a row | Pass | `test_editing_a_published_row_sends_it_back_to_review`: an edit takes the row off the site until a publisher approves it, which records the new verification date shown on /compatibility |
| A23 Performance | Partly measured | Budgets met by size: CSS 5.5 KB gzip (budget 80), custom JS 5.5 KB gzip (budget 60), home HTML 5.0 KB gzip, largest image 34 KB (reader, below the fold, lazy). The hero has no image: its largest element is text. Lab score and field Core Web Vitals not measured |

## Deviations and answered findings

* **D1. Hallmark rule 58 (about 80 words per screen) fails on 18 deep pages.** The locked DESIGN.md of the handoff package asks for "a readable long-document layout rather than squeezing their facts into a marketing word limit" for technical detail, and the copy deck text is used as written. The home page and About pass. Cutting contracted copy was not done; the design owner should confirm this reading or ask for shorter copy.
* **REFLEX answered.** 44c/79 "hero ends early" on deep pages: the 03 spec prescribes a compact intro there, not a full-screen hero. 49b links wrapping at 320 px: long link labels (footer, guide titles) wrap by design. 77 "thin sections" and 59 gaps: closing next-step sections and the contact layout. 78: contact aside headings are small by design.
* **Fonts.** General Sans is loaded from Fontshare as in the design reference (system-sans fallback in the token). Self-hosting needs the licence confirmed; until then this is a recorded release deviation. General Sans has no Cyrillic, so Ukrainian pages use the system sans throughout (D2).
* **D2. Ukrainian typeface.** System sans instead of General Sans on `/uk/` pages; a licensed face with Cyrillic would restore the design voice.
* **D3. Translations not reviewed by native speakers.** Written in this task against a shared glossary and the claim limits, checked automatically for markup, placeholders and coverage; a person should read each language before release. Legal pages, archived articles and team biographies are English in every language, with a note.
* **Certifications.** FCC and ISED identifiers were carried over from the previous page; the FCC aggregator answered with a bot check, so those records were not re-opened. CE, Google Smart Tap and Apple ECP2 documents were read and described as they state.
* **Archived articles.** Kept with original text, date and author, plus an archive note; they contain statements broader than the claim register (listed in `registers/claims.md`).

## Static review copy (GitHub Pages)

Published by the `Publish test preview` workflow and checked on the live URL https://dolzhenkovital.github.io/smartphonekey-site-v2/ on 27 October 2026: all 25 page URLs, the CSS, scripts, images and a certificate PDF answer 200; an unknown URL answers 404 with the 2.0 not-found page; pages carry `noindex, nofollow` and the preview banner; the home setup tool updates in place and General Sans loads.

Built from the same Odoo templates with `spk_website_v2.preview_mode` on: banner, `noindex` on every page, `Disallow: /`, and a contact form that runs its checks but never sends (button disabled without JavaScript; with it, a "test preview" message instead of sending). 190 pages in five languages. Limits of static hosting: redirects are noindex refresh pages instead of 301s, the setup result needs JavaScript (the server-rendered no-JS result exists only in Odoo), `hreflang` alternates are omitted because the copy is noindex, and links to the instruction site and portal go to the current Odoo host, spkey.odoo.com (the instruction page opens in the page's language through `?lang=`).
