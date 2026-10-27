# Release and rollback checklist

Preparing this site does not authorise a production release, a DNS change, real lock actions or messages to customers. Each step below needs the release owner's go-ahead in the actual release scope.

## Before stage

- [ ] Branch in spk-odoo named for the Jira task; `addons/spk_website_v2` copied in; no other module changed.
- [ ] spk-odoo PR rules: changelog entry in `addons/smartphonekey/CHANGELOG.md` with `> Guide: n/a`; `make lint`, `lint-actions`, `lint-assets`, `lint-tests`, `lint-views`, `lint-guide`, `lint-i18n`, `lint-scss`; Odoo.sh build with `make test` (grep the log: tests actually ran).
- [ ] Website settings: sales team and salesperson for website leads; Cloudflare Turnstile keys if the baseline uses them.
- [ ] Owner decisions recorded for the open items in `IMPLEMENTATION-STATUS.md` (each has a fallback; none blocks the release except lead routing).

## On stage (neutralized copy)

- [ ] Module installed/updated; revision noted.
- [ ] Stage answers `noindex` and `Disallow: /` (neutralized database) and is access-restricted.
- [ ] Every route in `registers/routes.json` answers as listed; every URL in `registers/redirects.json` answers as listed; `/adminpanel` reaches the portal login; `/guide-for-usage-and-installation` and `/instructions/*` render unchanged in at least two languages.
- [ ] Portal login, the SPK Portal and the guides show no 2.0 styles or scripts.
- [ ] One identified test enquiry: exactly one lead with the website context; a resubmission does not add a second; no email to real recipients unless the test procedure allows it.
- [ ] Visual check at 1440, 768 and 390 px against `qa/screenshots/`.

## Cutover (production, only within release authorisation)

- [ ] Backup: database, filestore, configuration. Record current domain, redirects, robots setting and the previous module state.
- [ ] Baseline: export Search Console / Bing URLs, queries, clicks and impressions if access exists; otherwise record "unavailable" and start the baseline after launch.
- [ ] Supplement `registers/redirects.json` with live history (Webflow redirect settings, backlinked and indexed URLs) and add any missing mapping.
- [ ] `spk_website_v2.enabled` on (default), `spk_website_v2.preview_mode` off, `database.is_neutralized` false.
- [ ] If the domain moves from Webflow: DNS only when authorised; one canonical host with HTTP and www redirected to `https://smartphonekey.com`.
- [ ] Verify on the live host: revision, HTTPS, canonical host, the route list, redirects, robots, sitemap, Open Graph image, no `noindex`, the real UI, one identified test lead.
- [ ] Submit the sitemap in the verified webmaster accounts.

## After

- [ ] Watch the first hour and the next business day: 404s, enquiry failures, portal regressions.
- [ ] 30/60/90-day review per 06/12 (coverage, non-brand discovery, setup and compatibility use, enquiry types).

## Rollback

Triggers: broken primary routes, persistent enquiry/CRM failure, exposed private content, marketing CSS on the portal, a wrong critical claim.

1. Set the system parameter `spk_website_v2.enabled` to `False` (Settings > Technical > System Parameters). Every URL returns to the AP-428 site immediately; no data is touched. Tested by `test_switch_hands_the_site_back_to_the_baseline`.
2. If the module itself must go, uninstall it only after exporting leads: uninstalling drops the website-enquiry columns from `crm.lead` (the leads stay, the typed context goes). Never restore an older database over newly received leads.
3. Recheck robots, `noindex` and canonicals after rolling back.

## Added for release 18.0.3.0.0 (27 October 2026)

* The upgrade runs `migrations/18.0.3.0.0/post-migrate.py`, which reloads the claim register, the compatibility rows and the four guides and overwrites editor changes to those records: export any editor changes first and re-apply them afterwards.
* Load the module with `-u spk_website_v2 --i18n-overwrite` so the rewritten French, German, Spanish and Ukrainian catalogues replace the old translations (a plain `-u` keeps them).
* On stage, before cutover: the instruction routes (`/guide-for-usage-and-installation`, `/instructions/*`) answer 200 from the `smartphonekey` module; every translated page carries five `hreflang` alternates plus `x-default` with preview mode off; the Manrope files under `/spk_website_v2/static/src/fonts/` are served; the preview banner is absent.
