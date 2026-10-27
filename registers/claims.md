# Claim register: where each claim is used

Baseline: the handoff register reviewed 2026-10-26. The same 20 records ship as `spk.website.claim` data (`addons/spk_website_v2/data/website_claims.xml`) so editors maintain them in Odoo. Evidence references (P01–P18, S10) point to the internal source register, which is not part of this repository.

Publication states: **public_scoped** (published with its limits), **fallback_only** (only the fallback sentence), **omit_numeric** (no number anywhere), **availability_enquiry** (ask-about-availability wording), **document_links_only** (documents, no badge).

| ID | Capability | Evidence | Publication | What the site says, and where | Gate still open |
|---|---|---|---|---|---|
| C01 | Multi-site access management | documented | public_scoped | Sites, people, credentials and devices: home, /platform, /platform/access-management | None |
| C02 | Scoped local management | documented | public_scoped | Local administrators "for the areas they manage"; screens depend on permissions: /platform/access-management, /solutions/* | None |
| C03 | LTE and Wi-Fi variants | owner-stated | public_scoped | Two connection options; LTE row says "No automatic switch to Wi-Fi is implied": /products/readers, LTE vs Wi-Fi guide, compatibility rows | SKU, region and SIM details not published |
| C04 | Integrated access controller | owner-stated | public_scoped | "combine credential reading with an integrated access controller", always with power, lock hardware and wiring still required: home, /products/readers | None |
| C05 | Card programming | documented | public_scoped | Only MIFARE Classic and MIFARE DESFire EV3; built-in programmer "where available": /products/readers, /compatibility, MIFARE guide, setup rule | No memory sizes, EV1/EV2 or other families (tested: `test_claim_scope_on_the_new_pages`) |
| C06 | Wallet and physical credentials | documented | public_scoped | Supported wallet credentials and physical NFC keys; no battery-reserve claim: /compatibility, /platform/access-management, apps page | Phone and OS matrix |
| C07 | Operational visibility | code-supported | public_scoped | Requested vs confirmed; "does not prove a person passed through or the door opened": /platform, offline guide, /security | None |
| C08 | Offline key queue | code-supported | public_scoped | "Some key changes"; "a revocation made while a reader is offline is pending, not enforced": /platform/access-management, offline guide, /security | None |
| C09 | Camera management | code-supported | public_scoped | "supported cameras ... check model compatibility and service scope": /solutions/property-managers | No camera compatibility row published |
| C10 | Matter capabilities | code-supported | public_scoped | Capability-based; commissioning does not prove every command: /compatibility, /platform/automation, Matter guide | Third-party model list after testing |
| C11 | Scenario Builder | code-supported | public_scoped | "Current scenarios use one hub and its commissioned devices": home, /platform/automation, /compatibility, setup rule | None |
| C12 | Hub-mediated reader connection | documented | public_scoped | "Supported reader configurations can connect through a Matter hub"; not a range or failover guarantee: /compatibility | None |
| C13 | Reader Matter/Thread roles | owner-stated | fallback_only | Only "confirm model and firmware" / "discuss supported Matter and Thread roles": /products/readers, /compatibility. The role row exists in review state and cannot be published (tested) | Hardware-role matrix per revision and firmware |
| C14 | Shared internet uplink | owner-stated | fallback_only | FAQ: "Supported hub and reader configurations can use a shared network path ... confirmed for the installed hardware". Matter guide topology labelled "Example topology. Deployment depends on configuration." | Topology test: gateway loss, node limits, multi-hop |
| C15 | Up to 80 m link distance | owner-stated | omit_numeric | No number anywhere (tested); "Coverage depends on the building, placement and radio conditions" | Reproducible model-specific range report |
| C16 | QR intercom | documented | public_scoped | Scan, follow guest instructions, contact, outcome; marketing site is not a door interface: /platform/visitor-access | None |
| C17 | AI Concierge v2 | release-gated | availability_enquiry | "Ask about the version and availability"; "features and rollout status vary by deployment": /platform/visitor-access | Versioned production release and acceptance |
| C18 | Monitoring alerts | code-supported | public_scoped | "Alerts require configuration; they do not replace an agreed support process": /platform/access-management, offline guide | None |
| C19 | Integrations | code-supported | public_scoped | "Integration" is an enquiry type; partner options "depend on the agreed offering": /solutions/integrators, /contact | No API tier, endpoint or SLA published |
| C20 | Certifications | unverified | document_links_only | /certifications lists each document with its issuer and what it states; no badges or umbrella claims. The Apple ECP2 file is labelled as a SmartphoneKey company document | FCC and ISED records were copied from the previous page and not re-opened here (the FCC aggregator shows a bot check); hardware owner to confirm |

## Content outside the register

* **Archived blog articles** (`/post/*`) keep their original text, which predates the register and includes broader statements (for example universal Matter compatibility, app-free entry, "simple setup"). Each carries an archive note pointing to the current scoped pages. Owner decision per article: keep, edit (and set a modification date) or retire.
* **Team roles** are as published on Webflow; `role_checked_on` is empty for all nine people.
* **ChatGPT app** (apps page): described only as "The actions available depend on your account." No register entry exists; product owner to add one before the page says more.
