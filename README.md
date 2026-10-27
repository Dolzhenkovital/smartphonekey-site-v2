# SmartphoneKey website 2.0

The smartphonekey.com redesign as an Odoo 18 addon: an **access control management platform** site (sites, people, credentials, responsibilities, readers and connected-device workflows), with an ungated setup guide, a compatibility centre, buyer guides, CRM enquiries, and the search foundations to go with them.

**Test preview:** https://dolzhenkovital.github.io/smartphonekey-site-v2/ — a static copy of the pages Odoo renders, marked noindex. Its contact form never sends anything. It is a review copy, not the live site.

## What is here

| Folder | Contents |
|---|---|
| `addons/spk_website_v2` | The addon. Depends on `spk_website` (the AP-428 Webflow port with the AP-429 homepage switch) from the SmartphoneKey Odoo repository, and on `website_crm` |
| `dev/` | Local test environment: Odoo 18 and PostgreSQL in Docker |
| `tools/` | Content import from the Webflow export, static export and link check, concurrency check, screenshots |
| `registers/` | Routes, the 34 Webflow URLs and what each now answers, where each product claim is used |
| `qa/`, `QA-REPORT.md` | Test, lint and browser evidence against acceptance criteria A01–A23 |
| `IMPLEMENTATION-STATUS.md` | Decisions, integration points, fallbacks in effect, open items |
| `RELEASE-CHECKLIST.md` | Stage, cutover and rollback |
| `preview/` | The static review copy GitHub Pages serves |

## Run it locally

Needs Docker and a checkout of the SmartphoneKey Odoo repository on a branch that contains `addons/spk_website` (AP-428/AP-429).

```bash
cd dev
SPK_BASELINE_ADDONS=/path/to/spk-odoo/addons docker compose up -d db
SPK_BASELINE_ADDONS=/path/to/spk-odoo/addons docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -i spk_website_v2 --stop-after-init
SPK_BASELINE_ADDONS=/path/to/spk-odoo/addons docker compose up -d odoo
```

Then open http://127.0.0.1:8069/. Tests:

```bash
SPK_BASELINE_ADDONS=/path/to/spk-odoo/addons docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -u spk_website_v2 --test-enable --test-tags /spk_website_v2 --stop-after-init
```

On Git Bash for Windows, prefix these with `MSYS_NO_PATHCONV=1`.

## Rebuild the test preview

Set the system parameter `spk_website_v2.preview_mode` to `True` on the local instance (it adds the banner, `noindex` and turns sending off), then:

```bash
python tools/export_static.py --odoo http://127.0.0.1:8069 --out preview --base /smartphonekey-site-v2 --external https://spkey.odoo.com
python tools/check_static.py preview --base /smartphonekey-site-v2
```

Commit `preview/`; the Pages workflow publishes it.

## Settings the addon reads

| System parameter | Default | Effect |
|---|---|---|
| `spk_website_v2.enabled` | on | `False` hands every URL back to the AP-428 site (rollback switch) |
| `spk_website_v2.preview_mode` | off | Review copy: banner, `noindex`, `Disallow: /`, the form never stores |
| `spk_website_v2.booking_url` | none | Optional "Choose a time to talk" link after an enquiry; HTTPS only |
| `spk_website_v2.booking_hosts` | `cal.com` | Hosts allowed for that link |

Content editors work in Website > Configuration > SmartphoneKey content (resources, compatibility rows, claim register, team pages). Editors change text; only the publisher group publishes.
