# SmartphoneKey website 2.0: mechanical inventory, 2026-10-27

Read-only inventory for the redesign. Workspace `C:\Project\Development\SmartphoneKey_site`; addon `implementation/addons/spk_website_v2`. Nothing was edited except this file. `export/private` and `.env` were not opened. All counts were produced by script from the files named; visual descriptions of images come from looking at contact sheets and video frames. The four public pages in section 3d were fetched with read-only GET.

**Snapshot.** Everything below that concerns the addon (strings, line numbers, tests, routes) was read from git commit `45b3296` of `implementation/` (HEAD), exported read-only with `git archive` to a scratch folder. While this inventory ran, another process was editing the working tree: at 12:14 (local time) `git status` showed uncommitted changes in `addons/spk_website_v2/data/website_claims.xml`, `data/website_compatibility.xml`, `data/website_resources.xml`, `site_content.py` and `registers/claims.md` (an owner clarification on card programming is being applied), plus untracked `addons/spk_website_v2/static/src/fonts/` and `qa/baseline-45b3296/`. The views, tests, models, controllers and the `.pot`/`.po` catalogues are identical to HEAD. Line numbers in those five edited files therefore refer to HEAD, and will have moved in the working tree. Section 1.2 states for each device-implying English line whether the same text is still in the working tree at the time of writing (12:17).

Conventions: `.pot`/`.po` line numbers are the line of the `msgid` keyword. Soft hyphens (U+00AD, inserted by `tools/i18n_soft_hyphens.py`) are removed from the `.po` msgstr text shown here, so the raw files contain extra invisible characters inside those words.

## 1. Programmer phrases

Owner position (from the task): SmartphoneKey does not support third-party card-programming devices; cards are programmed through the reader's own capability. "Device-implying" below means a string that names or implies an external, compatible or separate programming device, programmer or programming hardware. Generic uses of "card programming" / "program" that name no device are listed separately (1.5).

### 1.1 Totals

| Language / file | Device-implying strings | Generic "programming" strings (no device named) |
|---|---|---|
| English: `i18n/spk_website_v2.pot` msgids | 10 | 19 |
| English: source lines in views, data, site_content.py, setup_guide.py, models, controllers | 14 lines in 5 files | 29 lines in 10 files |
| French: `i18n/fr.po` | 10 | 19 |
| German: `i18n/de.po` | 10 | 19 |
| Spanish: `i18n/es.po` | 10 | 19 |
| Ukrainian: `i18n/uk.po` | 10 | 19 |
| **Total device-implying hits in the four .po files** | **40** |  |

Every device-implying msgid is translated in all four languages, so each language carries the same 10 strings. In fr and es the phrase "compatible programming hardware and firmware" is translated as "matériel et firmware de programmation compatibles" / "hardware y firmware de programación compatibles" (semantic hit, no literal "appareil/dispositivo"). A second pass with language-specific device terms over every msgstr found no hit outside these 10 msgids; the Ukrainian pattern `програм` also matches "мікропрограма" (firmware) and the German pattern "beschreib" matched "beschreibt": those are false positives and are not counted.

### 1.2 English sources: device-implying lines

| File:line (HEAD) | Text (first 120 chars) | Catalogue | Working tree at 12:17 |
|---|---|---|---|
| `views/platform.xml:80` | `Card programming depends on the card family and the programming device.` | .pot:1638 | unchanged |
| `views/products.xml:27` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | .pot:4685 | unchanged |
| `views/products.xml:193` | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | .pot:5984 | unchanged |
| `data/website_claims.xml:55` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with compatible programming hardware and firmware.` | not in .pot (claim register, backend only, not translated) | text no longer present |
| `data/website_claims.xml:56` | `No EV1/EV2 or memory-size inference; built-in programmer where available.` | not in .pot (claim register, backend only, not translated) | text no longer present |
| `data/website_compatibility.xml:14` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | .pot:2171 | text no longer present |
| `data/website_compatibility.xml:26` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | .pot:2171 | text no longer present |
| `data/website_compatibility.xml:52` | `Programming a new card needs a supported card family and programming device.` | .pot:4698 | text no longer present |
| `data/website_resources.xml:59` | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | .pot:5966 | text no longer present |
| `data/website_resources.xml:71` | `Programming: a supported programming device writes a SmartphoneKey credential to a supported card.` | .pot:701 | text no longer present |
| `data/website_resources.xml:82` | `MIFARE ClassicProgramming through the Admin Panel with a compatible programming device, including the reader's built-in` | .pot:4704 | text no longer present |
| `data/website_resources.xml:83` | `MIFARE DESFire EV3Programming through the Admin Panel with a compatible programming device, including the reader's built` | .pot:4704 | text no longer present |
| `data/website_resources.xml:89` | `Choose the programming device and the card type.` | .pot:1824 | text no longer present |
| `data/website_resources.xml:90` | `Tap the card on the programmer.` | .pot:5794 | text no longer present |

No device-implying wording exists in `site_content.py` (only generic: lines 103, 113, 421, 479-480, 570, and 389 in the setup-link label), `setup_guide.py`, `models/*.py` (generic only), `controllers/*.py`, `rendering.py` or `static/src/js/*.js`; none in `data/website_posts.xml` or `data/website_team.xml`.

The `.pot` and `.po` files in the working tree are still the HEAD versions, so the 10 msgids and 40 translations below stay in the catalogues until they are rebuilt (`tools/i18n_build.py`).

### 1.3 English msgids in `spk_website_v2.pot` (device-implying)

| Line | msgid (first 120 chars) | Source record / template |
|---|---|---|
| pot:701 | `<strong>Programming</strong>: a supported programming device writes a SmartphoneKey credential to a supported card.` | `resource_mifare body` |
| pot:1638 | `Card programming depends on the card family and the programming device.` | `view page_platform` |
| pot:1824 | `Choose the programming device and the card type.` | `resource_mifare body` |
| pot:2171 | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | `compat_mifare_classic capabilities`, `compat_mifare_desfire_ev3 capabilities` |
| pot:4685 | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | `view page_readers` |
| pot:4698 | `Programming a new card needs a supported card family and programming device.` | `compat_physical_keys limitations` |
| pot:4704 | `Programming through the Admin Panel with a compatible programming device, including the reader's built-in programmer whe` | `resource_mifare body` |
| pot:5794 | `Tap the card on the programmer.` | `resource_mifare body` |
| pot:5966 | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | `resource_mifare direct_answer` |
| pot:5984 | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | `view page_compatibility` |

### 1.4 Translations of those msgids

#### French (`i18n/fr.po`): 10 hits

| File:line | msgid (120) | msgstr (160) | Device term in msgstr |
|---|---|---|---|
| `fr.po:737` | `<strong>Programming</strong>: a supported programming device writes a SmartphoneKey credential to a supported card.` | `<strong>Programmation</strong> : un appareil de programmation pris en charge écrit un identifiant d'accès SmartphoneKey sur une carte prise en charge.` | appareil de programmation |
| `fr.po:1770` | `Card programming depends on the card family and the programming device.` | `La programmation des cartes dépend de la famille de cartes et de l'appareil de programmation.` | appareil de programmation |
| `fr.po:1988` | `Choose the programming device and the card type.` | `Choisissez l'appareil de programmation et le type de carte.` | appareil de programmation |
| `fr.po:2366` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | `Programmation des identifiants d'accès via le processus de l'Admin Panel avec un appareil de programmation SmartphoneKey compatible, y compris le programmateur` | appareil de programmation; programmateur |
| `fr.po:5066` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | `Programmez des cartes MIFARE Classic et MIFARE DESFire EV3 prises en charge avec un appareil de programmation compatible, y compris le programmateur intégré du` | appareil de programmation; programmateur |
| `fr.po:5083` | `Programming a new card needs a supported card family and programming device.` | `La programmation d'une nouvelle carte nécessite une famille de cartes et un appareil de programmation pris en charge.` | appareil de programmation |
| `fr.po:5091` | `Programming through the Admin Panel with a compatible programming device, including the reader's built-in programmer whe` | `Programmation via l'Admin Panel avec un appareil de programmation compatible, y compris le programmateur intégré du lecteur lorsqu'il est disponible` | appareil de programmation; programmateur |
| `fr.po:6269` | `Tap the card on the programmer.` | `Approchez la carte du programmateur.` | programmateur |
| `fr.po:6456` | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | `Les processus de programmation documentés mentionnent MIFARE Classic et MIFARE DESFire EV3. Un programmateur compatible ou le programmateur intégré au lecteur p` | programmateur |
| `fr.po:6483` | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | `Les processus documentés prennent en charge MIFARE Classic et MIFARE DESFire EV3 avec un matériel et un firmware de programmation compatibles. Confirmez la vari` | matériel et un firmware de programmation compatibles |

#### German (`i18n/de.po`): 10 hits

| File:line | msgid (120) | msgstr (160) | Device term in msgstr |
|---|---|---|---|
| `de.po:737` | `<strong>Programming</strong>: a supported programming device writes a SmartphoneKey credential to a supported card.` | `<strong>Programmieren</strong>: Ein unterstütztes Programmiergerät schreibt SmartphoneKey-Zutrittsdaten auf eine unterstützte Karte.` | Programmiergerät |
| `de.po:1773` | `Card programming depends on the card family and the programming device.` | `Die Kartenprogrammierung hängt von der Kartenfamilie und dem Programmiergerät ab.` | Programmiergerät |
| `de.po:1994` | `Choose the programming device and the card type.` | `Wählen Sie das Programmiergerät und den Kartentyp.` | Programmiergerät |
| `de.po:2372` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | `Programmierung von Zutrittsmedien über den Workflow im Admin Panel mit einem kompatiblen SmartphoneKey-Programmiergerät, einschließlich des im Leser integrierte` | Programmiergerät; Programmiergeräts |
| `de.po:5075` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | `Programmieren Sie unterstützte Karten vom Typ MIFARE Classic und MIFARE DESFire EV3 mit einem kompatiblen Programmiergerät, einschließlich des im Leser integrie` | Programmiergerät; Programmiergeräts |
| `de.po:5092` | `Programming a new card needs a supported card family and programming device.` | `Zum Programmieren einer neuen Karte sind eine unterstützte Kartenfamilie und ein unterstütztes Programmiergerät erforderlich.` | Programmiergerät |
| `de.po:5101` | `Programming through the Admin Panel with a compatible programming device, including the reader's built-in programmer whe` | `Programmierung über das Admin Panel mit einem kompatiblen Programmiergerät, einschließlich des im Leser integrierten Programmiergeräts, sofern verfügbar` | Programmiergerät; Programmiergeräts |
| `de.po:6280` | `Tap the card on the programmer.` | `Halten Sie die Karte an das Programmiergerät.` | Programmiergerät |
| `de.po:6468` | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | `Die dokumentierten Programmier-Workflows nennen MIFARE Classic und MIFARE DESFire EV3. Ein kompatibles Programmiergerät oder das unterstützte, im Leser integrie` | Programmiergerät |
| `de.po:6496` | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | `Die dokumentierten Workflows unterstützen MIFARE Classic und MIFARE DESFire EV3 mit kompatibler Programmier-Hardware und Firmware. Bestätigen Sie vor der Bestel` | Programmier-Hardware |

#### Spanish (`i18n/es.po`): 10 hits

| File:line | msgid (120) | msgstr (160) | Device term in msgstr |
|---|---|---|---|
| `es.po:733` | `<strong>Programming</strong>: a supported programming device writes a SmartphoneKey credential to a supported card.` | `<strong>Programación</strong>: un dispositivo de programación compatible escribe una credencial de SmartphoneKey en una tarjeta compatible.` | dispositivo de programación |
| `es.po:1763` | `Card programming depends on the card family and the programming device.` | `La programación de tarjetas depende de la familia de tarjetas y del dispositivo de programación.` | dispositivo de programación |
| `es.po:1980` | `Choose the programming device and the card type.` | `Elija el dispositivo de programación y el tipo de tarjeta.` | dispositivo de programación |
| `es.po:2358` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | `Programación de credenciales mediante el flujo de trabajo del Admin Panel con un dispositivo de programación SmartphoneKey compatible, incluido el programador i` | dispositivo de programación; programador |
| `es.po:5045` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | `Programe las tarjetas MIFARE Classic y MIFARE DESFire EV3 admitidas con un dispositivo de programación compatible, incluido el programador integrado del lector` | dispositivo de programación; programador |
| `es.po:5062` | `Programming a new card needs a supported card family and programming device.` | `Para programar una tarjeta nueva se necesitan una familia de tarjetas y un dispositivo de programación compatibles.` | dispositivo de programación |
| `es.po:5070` | `Programming through the Admin Panel with a compatible programming device, including the reader's built-in programmer whe` | `Programación a través del Admin Panel con un dispositivo de programación compatible, incluido el programador integrado del lector cuando esté disponible` | dispositivo de programación; programador |
| `es.po:6248` | `Tap the card on the programmer.` | `Acerque la tarjeta al programador.` | programador |
| `es.po:6434` | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | `Los flujos de trabajo de programación documentados mencionan MIFARE Classic y MIFARE DESFire EV3. Un programador compatible o el programador integrado admitido` | programador |
| `es.po:6461` | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | `Los flujos de trabajo documentados admiten MIFARE Classic y MIFARE DESFire EV3 con hardware y firmware de programación compatibles. Confirme la variante exacta` | hardware y firmware de programación compatibles |

#### Ukrainian (`i18n/uk.po`): 10 hits

| File:line | msgid (120) | msgstr (160) | Device term in msgstr |
|---|---|---|---|
| `uk.po:734` | `<strong>Programming</strong>: a supported programming device writes a SmartphoneKey credential to a supported card.` | `<strong>Програмування</strong>: підтримуваний пристрій для програмування записує ідентифікатор доступу SmartphoneKey на підтримувану картку.` | (see note 1.1) |
| `uk.po:1761` | `Card programming depends on the card family and the programming device.` | `Програмування карток залежить від сімейства карток і пристрою для програмування.` | пристрою для програмування |
| `uk.po:1976` | `Choose the programming device and the card type.` | `Оберіть пристрій для програмування та тип картки.` | (see note 1.1) |
| `uk.po:2351` | `Credential programming through the Admin Panel workflow with a compatible SmartphoneKey programming device, including th` | `Програмування ідентифікаторів доступу через робочий процес в Admin Panel за допомогою сумісного пристрою для програмування SmartphoneKey, зокрема вбудованого пр` | пристрою для програмування; програматора |
| `uk.po:5031` | `Program supported MIFARE Classic and MIFARE DESFire EV3 cards with a compatible programming device, including the reader` | `Програмуйте підтримувані картки MIFARE Classic і MIFARE DESFire EV3 за допомогою сумісного пристрою для програмування, зокрема вбудованого програматора зчитувач` | пристрою для програмування; програматора |
| `uk.po:5048` | `Programming a new card needs a supported card family and programming device.` | `Для програмування нової картки потрібні підтримувані сімейство карток і пристрій для програмування.` | (see note 1.1) |
| `uk.po:5056` | `Programming through the Admin Panel with a compatible programming device, including the reader's built-in programmer whe` | `Програмування через Admin Panel за допомогою сумісного пристрою для програмування, зокрема вбудованого програматора зчитувача, де він є` | пристрою для програмування; програматора |
| `uk.po:6225` | `Tap the card on the programmer.` | `Прикладіть картку до програматора.` | програматора |
| `uk.po:6408` | `The documented programming workflows name MIFARE Classic and MIFARE DESFire EV3. A compatible programmer or the supporte` | `Задокументовані процеси програмування називають MIFARE Classic і MIFARE DESFire EV3. Сумісний програматор або підтримуваний вбудований програматор зчитувача зап` | програматор |
| `uk.po:6435` | `The documented workflows support MIFARE Classic and MIFARE DESFire EV3 using compatible programming hardware and firmwar` | `Задокументовані процеси підтримують MIFARE Classic і MIFARE DESFire EV3 із використанням сумісного обладнання для програмування та мікропрограми. Перед замовлен` | обладнання для програмування |

### 1.5 Generic "programming" strings (no device named; not counted above)

Same msgids exist in every language. Line numbers are msgid lines.

| msgid (first 100 chars) | Lines |
|---|---|
| `<span class="muted">Documented card programming, digital credentials, Matter capabilities and networ` | pot:169 fr:171 de:169 es:169 uk:169 |
| `A card that a reader can detect is not automatically a card that SmartphoneKey can program.` | pot:972 fr:1027 de:1025 es:1023 uk:1026 |
| `Card programming` | pot:1633 fr:1765 de:1768 es:1758 uk:1756 |
| `Cards within one family share a common basis, but chip-level compatibility is not evidence that Smar` | pot:1651 fr:1785 de:1788 es:1778 uk:1776 |
| `Documented card programming workflows` | pot:2402 fr:2618 de:2624 es:2608 uk:2602 |
| `How an operator programs a card` | pot:3059 fr:3325 de:3333 es:3312 uk:3304 |
| `MIFARE Classic and DESFire EV3 Programming \| SmartphoneKey` | pot:3785 fr:4091 de:4101 es:4075 uk:4066 |
| `Physical card programming` | pot:4485 fr:4859 de:4868 es:4839 uk:4827 |
| `Physical card programming.` | pot:4490 fr:4864 de:4873 es:4844 uk:4832 |
| `Program` | pot:4680 fr:5061 de:5070 es:5040 uk:5026 |
| `Program supported physical cards.` | pot:4693 fr:5078 de:5087 es:5057 uk:5043 |
| `Reading, programming and assigning access` | pot:4888 fr:5288 de:5298 es:5266 uk:5251 |
| `See the documented physical-card programming workflows and understand why card variants, credential` | pot:5149 fr:5561 de:5571 es:5539 uk:5523 |
| `Supported configurations add card programming and connected-device functions.` | pot:5743 fr:6207 de:6219 es:6186 uk:6165 |
| `Which NFC cards can SmartphoneKey program?` | pot:6821 fr:7413 de:7435 es:7386 uk:7355 |
| `Which physical cards can be programmed?` | pot:6833 fr:7427 de:7449 es:7400 uk:7369 |
| `Compare SmartphoneKey LTE and Wi-Fi reader configurations, integrated control, supported card progra` | pot:7390 fr:8038 de:8053 es:8003 uk:7976 |
| `Check documented MIFARE Classic and DESFire EV3 programming, Matter capabilities and the configurati` | pot:7404 fr:8055 de:8070 es:8020 uk:7992 |
| `Confirm the card family and credential format. The documented programming workflows cover MIFARE Cla` | pot:7678 fr:8368 de:8387 es:8336 uk:8302 |

English source lines containing "program" but no device wording (29): `views/components.xml:21`; `views/home.xml:81`; `views/products.xml:26`; `views/products.xml:28`; `views/products.xml:137`; `views/products.xml:147`; `views/products.xml:151`; `views/products.xml:192`; `views/resources.xml:37`; `data/website_claims.xml:52`; `data/website_compatibility.xml:13`; `data/website_compatibility.xml:25`; `data/website_resources.xml:55`; `data/website_resources.xml:56`; `data/website_resources.xml:57`; `data/website_resources.xml:67`; `data/website_resources.xml:74`; `data/website_resources.xml:77`; `data/website_resources.xml:95`; `models/website_compatibility.py:14`; `models/website_compatibility.py:22`; `controllers/main.py:8`; `site_content.py:103`; `site_content.py:113`; `site_content.py:389`; `site_content.py:421`; `site_content.py:479`; `site_content.py:480`; `site_content.py:570`.

### 1.6 Other notes

* The claim register rows (`data/website_claims.xml:55-56`, claim C05, and `implementation/registers/claims.md:15`) carry the same "compatible programming hardware" / "built-in programmer" wording; they are staff-facing and not translated, but they are the source the public copy follows.
* Outside the addon (not searched line by line, listed for reference), files containing "programmer" or "programming device/hardware": `docs/site-v2/02-EVIDENCE-AND-CLAIMS.md`, `04-COPY-DECK-EN.md`, `08-JIRA-TICKET.md`, `11-SOURCES.md`, `CLAUDE-MASTER-BRIEF-EN.md`, `FULL-BRIEF.md`, `data/claims.json`, `data/search-intents.json`, `skills/smartphonekey-site-content/references/evidence.md`, and `implementation/registers/claims.md`.
* The compatibility model labels the operation `program` as "Program" (`models/website_compatibility.py:22`, `site_content.py:570`) and the category as "Physical card programming" (`models/website_compatibility.py:14`); both are generic.

## 2. String inventory (`i18n/spk_website_v2.pot`)

### 2.1 Totals (unique msgids; words = whitespace-separated tokens of the English msgid after stripping HTML tags)

| Class | msgids | Approx. words | Note |
|---|---|---|---|
| Public pages: translated into fr, de, es, uk (`i18n_build.is_public`) | 795 | 7,015 | Each of fr/de/es/uk has exactly 795 non-empty msgstr, all inside this class; 0 public msgids untranslated |
| English-only on purpose: privacy policy and terms of service | 77 | 1,322 | templates `page_privacy_policy`, `page_terms_of_service` |
| English-only on purpose: posts (6 articles: bodies and name/description/seo_title/direct_answer) | 232 | 4,535 | records `post_*` |
| English-only on purpose: team biographies (9 members) | 22 | 1,113 | `spk.website.team.member,bio` |
| Backend / staff UI (field labels, selections, menus, constraints, model messages, backend views) | 115 | 382 | not shown on the public site, not translated |
| **All msgids** | **1241** | **14,367** | English-only on purpose in total: 331 msgids, 6,970 words |

Rule in `implementation/tools/i18n_build.py` `ENGLISH_ONLY_REFS`: `spk_website_v2.page_privacy_policy`, `spk_website_v2.page_terms_of_service`, `.post_`, `spk.website.team.member,bio`. A msgid that also occurs in a public source stays public (3 such msgids: shared labels). The same split drives `ENGLISH_ONLY` in `site_content.py` (`/privacy-policy`, `/terms-of-service`) and the post/team handling in `controllers/main.py`.

Unique public msgids by first source (a msgid used in several places is counted once, in the first source of this list):

| First source | msgids | Approx. words |
|---|---|---|
| page templates (`views/*.xml`) | 507 | 4,119 |
| code terms not already in a template (`site_content.py`) | 117 | 843 |
| guide bodies (`spk.website.resource,body`) | 112 | 1,284 |
| guide name/description/seo_title/direct_answer not already counted | 13 | 327 |
| compatibility rows not already counted | 29 | 378 |
| team job_title / photo_alt | 17 | 64 |
| **Total** | **795** | **7,015** |

### 2.2 By source reference group

A msgid used in several templates is counted in each of them, so the group counts add up to more than the unique totals above. "Translated" is per msgid (`is_public`): "yes" means all of the group's msgids are public, "partly" means some are shared with public sources.

#### Page templates (`model_terms:ir.ui.view,arch_db:spk_website_v2.<id>`)

| Template id | msgids | Words | Translated |
|---|---|---|---|
| `page_platform` | 49 | 441 | yes |
| `page_home` | 47 | 243 | yes |
| `page_terms_of_service` | 45 | 870 | English-only on purpose (1 shared with public sources) |
| `page_certifications` | 45 | 280 | yes |
| `page_contact` | 43 | 265 | yes |
| `page_privacy_policy` | 36 | 462 | English-only on purpose (1 shared with public sources) |
| `page_automation` | 36 | 285 | yes |
| `page_readers` | 36 | 476 | yes |
| `page_resources` | 31 | 210 | yes |
| `page_access_management` | 29 | 337 | yes |
| `page_setup` | 26 | 155 | yes |
| `page_property_managers` | 25 | 198 | yes |
| `page_compatibility` | 25 | 305 | yes |
| `page_integrators` | 22 | 207 | yes |
| `page_visitor_access` | 19 | 235 | yes |
| `reader_comparison` | 19 | 90 | yes |
| `page_security` | 17 | 163 | yes |
| `page_article` | 17 | 72 | yes |
| `page_apps` | 15 | 97 | yes |
| `header` | 9 | 12 | yes |
| `page_about` | 8 | 62 | yes |
| `compatibility_table` | 8 | 29 | yes |
| `page_thank_you` | 7 | 52 | yes |
| `footer` | 6 | 17 | yes |
| `page_404` | 6 | 20 | yes |
| `page_team_member` | 4 | 11 | yes |
| `view_spk_website_compatibility_form` | 3 | 5 | backend view, not translated |
| `layout` | 3 | 30 | yes |
| `view_spk_website_resource_form` | 2 | 4 | backend view, not translated |
| `breadcrumbs` | 1 | 1 | yes |
| `faq` | 1 | 1 | yes |
| `crm_lead_view_form_spk_website` | 1 | 2 | backend view, not translated |
| **Sum of rows** | **641** | **5637** |  |

#### Data records

| Source | msgids | Words | Translated |
|---|---|---|---|
| `spk.website.resource` body, post `post_how_smartphonekey_enhances_security_for_your_property` | 37 | 884 | English-only on purpose (1 shared with public sources) |
| `spk.website.resource` body, post `post_matter_standard_the_key_to_a_seamless_smart_home` | 53 | 686 | English-only on purpose |
| `spk.website.resource` body, post `post_smart_home_trends_2025_the_future_of_secure_and_connected_living` | 38 | 771 | English-only on purpose |
| `spk.website.resource` body, post `post_smartphonekey_official_launch` | 17 | 424 | English-only on purpose |
| `spk.website.resource` body, post `post_the_future_of_keyless_entry_why_its_time_to_upgrade_to_smartphonekey` | 38 | 868 | English-only on purpose (1 shared with public sources) |
| `spk.website.resource` body, post `post_welcome_to_smartphonekey_your_affordable_access_to_a_keyless_future` | 29 | 524 | English-only on purpose |
| `spk.website.resource` body, guide `resource_lte_vs_wifi` | 21 | 292 | yes |
| `spk.website.resource` body, guide `resource_matter_thread` | 37 | 423 | yes |
| `spk.website.resource` body, guide `resource_mifare` | 27 | 259 | yes |
| `spk.website.resource` body, guide `resource_offline` | 29 | 315 | yes |
| `spk.website.resource` field `seo_title`, guides (4 guides / 6 posts) | 4 | 36 | yes |
| `spk.website.resource` field `description`, guides (4 guides / 6 posts) | 4 | 70 | yes |
| `spk.website.resource` field `direct_answer`, guides (4 guides / 6 posts) | 4 | 215 | yes |
| `spk.website.resource` field `name`, guides (4 guides / 6 posts) | 4 | 26 | yes |
| `spk.website.resource` field `description`, posts (4 guides / 6 posts) | 6 | 119 | English-only on purpose |
| `spk.website.resource` field `name`, posts (4 guides / 6 posts) | 6 | 52 | English-only on purpose |
| `spk.website.resource` field `seo_title`, posts (4 guides / 6 posts) | 6 | 45 | English-only on purpose |
| `spk.website.resource` field `direct_answer`, posts (4 guides / 6 posts) | 6 | 166 | English-only on purpose |
| `spk.website.compatibility` field `capabilities` | 10 | 130 | yes |
| `spk.website.compatibility` field `limitations` | 11 | 222 | yes |
| `spk.website.compatibility` field `name` | 11 | 33 | yes |
| `spk.website.team.member` field `job_title` | 8 | 28 | yes |
| `spk.website.team.member` field `photo_alt` | 9 | 36 | yes |
| `spk.website.team.member` bio, `team_alex_sydorenko` | 2 | 84 | English-only on purpose |
| `spk.website.team.member` bio, `team_denys_merkulov` | 2 | 115 | English-only on purpose |
| `spk.website.team.member` bio, `team_ioannis_mavridis` | 3 | 137 | English-only on purpose |
| `spk.website.team.member` bio, `team_kate_vasylenko` | 3 | 202 | English-only on purpose |
| `spk.website.team.member` bio, `team_kostiantyn_dolzhenko` | 3 | 139 | English-only on purpose |
| `spk.website.team.member` bio, `team_lana_ostapenko` | 2 | 90 | English-only on purpose |
| `spk.website.team.member` bio, `team_oleksii_andrieiev` | 3 | 116 | English-only on purpose |
| `spk.website.team.member` bio, `team_vadym_sydorenko` | 2 | 120 | English-only on purpose |
| `spk.website.team.member` bio, `team_vitalii_dolzhenko` | 2 | 110 | English-only on purpose |

Claim-register records (`spk.website.claim`) have no translatable terms in the catalogue.

#### Code terms (`code:addons/spk_website_v2/...`)

| File | msgids | Words | Translated |
|---|---|---|---|
| `site_content.py` | 155 | 979 | yes |
| `models/website_claim.py` | 1 | 14 | backend model message, not translated |
| `models/website_resource.py` | 3 | 29 | backend model message, not translated |
| `models/website_compatibility.py` | 3 | 33 | backend model message, not translated |
| `models/website_team.py` | 1 | 11 | backend model message, not translated |

#### Backend model terms

| Reference type | msgids | Words | Translated |
|---|---|---|---|
| `model:ir.model.fields.selection` | 56 | 108 | backend, not translated (35 shared with public code terms) |
| `model:ir.model.constraint` | 4 | 26 | backend, not translated |
| `model:ir.model.fields` | 77 | 209 | backend, not translated (13 shared with public code terms) |
| `model:ir.actions.act_window` | 4 | 7 | backend, not translated (1 shared with public code terms) |
| `model:ir.ui.menu` | 5 | 9 | backend, not translated (1 shared with public code terms) |
| `model:ir.model` | 7 | 21 | backend, not translated |
| `model:res.groups` | 2 | 7 | backend, not translated |

## 3. Product-image assets

**Short answer:** no real Admin Panel or mobile-app screenshot exists in the workspace image libraries (3a-3c). The old-site images are phone mockups, 3D/composite device renders, illustrations and portraits; real reader photographs exist only inside three of the four videos (and the poster frame of the product video). Of the four public pages (3d), none has an `<img>` of an Admin Panel or app screen: the Admin Panel walkthrough is a scripted interactive mock with demo data, the Admin guide opens 11 small vector SVG sketches (13 in the repository), the mobile-app walkthrough renders 13 PNG app screens that its own source calls pre-release design mock-ups. The installation guide has real reader/exit-button/SIM/wiring images. See 3f for the sibling repository.

### 3a. `export/assets` (index.json + files)

`index.json` lists 128 files, all present in `export/assets/files` (no orphans): 52 image/svg+xml, 38 image/webp, 21 image/png, 9 image/jpeg, 4 video/mp4, 3 application/pdf, 1 application/vnd.openxmlformats-officedocument.wordprocessingml.document. The index `size` field is 0 for 4 entries, so sizes below are from the file system. Alt text in the index exists for 6 entries only (certificate, App Store/Google Play/ChatGPT icons and badges). Dimensions from PIL 12.2.0; video data from ffprobe.

Flags are my visual reading of each file (contact sheets). PHONE MOCKUP: a phone with a staged screen (Wallet pass, lock-screen notification, chat UI, camera feed). DEVICE RENDER: rendered or composited image of the unit/box, card, key tag, or hands holding a card or phone at a unit. ILLUSTRATION: icons, QR, chat bubble, 3D symbols. No raster file in `export/assets` carries camera EXIF data (1 of 68 has 3 generic tags), so a photograph cannot be told from a render by metadata. No row is a product UI screenshot (Admin Panel, mobile app).

| File (`export/assets/files/`) | Dimensions | KB | Alt in index | Alt on old pages | Referenced in `mirror/raw` HTML | Flag | What it shows |
|---|---|---|---|---|---|---|---|
| `6a72021c4de7e87a0f7f39bd_google-smarttap-2-1-compliance-certificate.jpeg` | 801x993 | 69.0 | Google Smart Tap 2.1 compliance certificate issued to SmartphoneKey Systems on May 22, 2025 | Google Smart Tap 2.1 compliance certificate issued to SmartphoneKey Systems on May 22, 2025 | certifications | DOCUMENT | Google Smart Tap 2.1 certificate, scanned page |
| `6a16fd0eb1e4c275dd0bdac7_App Store Icon.png` | 480x480 | 10.3 | Apple App Store | Download on the App Store | 32 old pages | LOGO/BADGE | App Store icon |
| `6a16fd0c390d07357cde5b7d_Google Play Icon.png` | 480x480 | 10.6 | Google Play | Get it on Google Play | 32 old pages | LOGO/BADGE | Google Play icon |
| `6a16f83971435c1aee26c09c_ChatGPT Logo.png` | 480x480 | 21.4 | Available on ChatGPT Apps | Available on ChatGPT; SmartphoneKey on ChatGPT | 32 old pages | LOGO/BADGE | ChatGPT logo |
| `6a16f8062d8f5c730d20102c_Google Play Badge.png` | 646x250 | 4.8 | Get it on Google Play | Get it on Google Play | apps-and-chatbot | LOGO/BADGE | Google Play badge |
| `69038f9fdb70dd13365ef8f8_1440х1080_ICP 2_ Airbnb hosts (7).jpg` | 808x438 | 147.1 | - | - | guide-for-usage-and-installation | ILLUSTRATION | Chat bubble "Hi! Got any questions? I'm happy to help." on dark green |
| `69038f5bcc8afa0a6c149032_1440х1080_ICP 2_ Airbnb hosts (6).jpg` | 808x438 | 148.8 | - | - | guide-for-usage-and-installation | ILLUSTRATION | QR code on a dark panel |
| `69038f22c51647ed105d8f2c_1440х1080_ICP 2_ Airbnb hosts (5).jpg` | 808x438 | 135.4 | - | - | guide-for-usage-and-installation | PHONE MOCKUP | Dark phone with chat bubbles (chat UI illustration) |
| `69038ee2adc81b5161ee33c9_1440х1080_ICP 2_ Airbnb hosts (4).jpg` | 808x438 | 139.9 | - | - | guide-for-usage-and-installation | PHONE MOCKUP | Phone lock screen with notification "Megan is calling to enter the apartments." |
| `6903855c7b67e7811dc4bd99_1440х1080_ICP 2_ Airbnb hosts (3).jpg` | 808x438 | 143.1 | - | - | guide-for-usage-and-installation | PHONE MOCKUP | Phone Wallet screen showing a SmartphoneKey pass |
| `690384cef00866500f84b14d_1440х1080_ICP 2_ Airbnb hosts (2).jpg` | 808x438 | 244.0 | - | - | guide-for-usage-and-installation | DEVICE RENDER | Hands passing a black SmartphoneKey card (render/composite) |
| `69036e89b74ee938a6655e65_1440х1080_ICP 2_ Airbnb hosts (1).jpg` | 808x438 | 184.2 | - | - | guide-for-usage-and-installation | DEVICE RENDER | Black product box/unit: KEY logo, phone-in-hand pictogram, "Scan to call" QR (render) |
| `68ffa3b03dbf94ecd0722881_Frame 1171276647.webp` | 2880x846 | 7.8 | - | - | not referenced | DECOR | Dark green gradient, wide |
| `68fa189cc78128827cb7247c_1440х1080_ICP 2_ Airbnb hosts (6).webp` | 1080x1106 | 69.6 | - | - | not referenced | PHONE MOCKUP | Hands holding a phone showing a camera feed |
| `68fa0e312b1770e357d3dccf_1440х1080_ICP 2_ Airbnb hosts (5).webp` | 1080x1106 | 68.0 | - | - | intercom-solution | ILLUSTRATION | 3D phone with up/down arrows |
| `68fa0df1491940172d8dc341_1440х1080_ICP 2_ Airbnb hosts (4).webp` | 1080x1106 | 57.9 | - | - | intercom-solution | PHONE MOCKUP | Phone with "SmartphoneKey Bot" chat (illustration) |
| `68fa0dc6c749456b59200156_1440х1080_ICP 2_ Airbnb hosts (3) (1).webp` | 1080x1106 | 78.9 | - | - | intercom-solution | ILLUSTRATION | Three round icons (lock, bell, camera) around the key logo |
| `68fa0d05627b1e922d5d6dbd_Frame 1171276658.webp` | 540x507 | 66.0 | - | - | intercom-solution | ILLUSTRATION | 3D cloud and phone data-transfer symbol, grey |
| `68fa0ce5a2aa632e40a6a351_Outline Cloud Data Transfer Symbol White.J01.2k 1.webp` | 540x507 | 71.5 | - | - | not referenced | ILLUSTRATION | 3D cloud and phone data-transfer symbol, grey (same motif) |
| `68fa0a772030ba1891c6727d_1440х1080_ICP 2_ Airbnb hosts (2) (1).webp` | 1080x1106 | 77.3 | - | - | facility-services, security-professionals | ILLUSTRATION | 3D cell tower icon |
| `68fa0a737b5d3a8cd1169299_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x1106 | 64.6 | - | - | facility-services, security-professionals | PHONE MOCKUP | Phone lock screen with notification |
| `68fa0a709e52acc3f4872863_1440х1080_ICP 2_ Airbnb hosts.webp` | 1080x1106 | 61.9 | - | - | security-professionals | ILLUSTRATION | QR code on a dark panel |
| `68fa0a6ba962874da8b29d31_1440х1080_ICP 2_ Airbnb hosts (3).webp` | 1080x1106 | 420.0 | - | - | facility-services, intercom-solution, security-professionals | PHONE MOCKUP | Phone Wallet screen mockup, dark |
| `68f8a42fb1318c82dfed8ff7_Security Shield Icon White.I01.2k 2 (1).png` | 1080x1014 | 350.5 | - | - | security-professionals | ILLUSTRATION | 3D padlock-in-shield icon, grey |
| `68f263b70127c72dedc41688_Ellipse 1.png` | 375x486 | 173.7 | - | - | not referenced | DECOR | Pale green gradient |
| `68f262f2d6d79fa921b10a54_Group 44334 (1).png` | 375x441 | 209.6 | - | - | smart-home-integrators | PHONE MOCKUP | Hand holding a phone with a Wallet pass (composite) |
| `68f2624c28d15e58e67dc71a_Group 44334.png` | 375x601 | 218.8 | - | - | not referenced | PHONE MOCKUP | Same, smaller crop |
| `68f261d2adf9ba48cb72182f_Frame 1171276759.png` | 375x852 | 55.2 | - | - | not referenced | DECOR | Dark logo-shaped tall background |
| `68f25476d4161cc0ba01790a_Frame 1171276723 (1).webp` | 1080x1014 | 72.3 | - | - | facility-services | ILLUSTRATION | 3D tower building, grey |
| `68f25404d6c66ad811595f6e_Monochrome Building.I01.2k 1.png` | 1080x1014 | 487.5 | - | - | not referenced | ILLUSTRATION | 3D tower building, grey |
| `68f25191ee04b281efc057e8_Frame 1171276723.png` | 2424x2260 | 2951.8 | - | - | not referenced | DEVICE RENDER | Product box/unit render on grey (2424x2260) |
| `68f24399ecdae67d56a919b3_2.jpg` | 345x259 | 31.2 | - | - | not referenced | DECOR | Dark green panel |
| `68f105ce9ab52dc805b3637e_Frame 57 (1).webp` | 484x484 | 23.1 | - | - | smart-home-integrators | ILLUSTRATION | Chat bubble illustration |
| `68f105854552b5450ca85721_1440х1080_ICP 2_ Airbnb hosts (2).webp` | 1080x1066 | 22.3 | - | smartphone keys | intercom-solution, smart-home-integrators | PHONE MOCKUP | Phone Wallet screen mockup |
| `68f102be655bdd0c45b475fe_Group 44332.webp` | 2418x1502 | 773.5 | - | - | not referenced | PHONE MOCKUP | Hand holding a phone with a Wallet pass, large |
| `68f0f69453c833bb6233453f_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x1106 | 64.6 | - | - | features, index | PHONE MOCKUP | Phone lock screen with notification |
| `68ef3e91e9d5f95764ccb893_Symbol Key.I01.2k 1.png` | 540x507 | 140.4 | - | - | not referenced | ILLUSTRATION | 3D key symbol, grey |
| `68ef3bf40aee0461bdb2ab77_1440х1080_ICP 2_ Airbnb hosts.webp` | 1080x1066 | 31.3 | - | - | not referenced | DEVICE RENDER | Product box/unit render, dark, QR visible |
| `68ef3801e6623f8e7cb27ed7_2.webp` | 2280x388 | 22.9 | - | - | not referenced | DECOR | Dark green gradient strip |
| `68ee5644741cd6f949c2c684_Frame 48.png` | 2880x1418 | 2201.9 | - | - | not referenced | DECOR | Dark green gradient, wide |
| `68ed0e40f9cf9c228c1e13f8_SmartphoneKey green logo.png` | 123x120 | 14.0 | - | - | not referenced | LOGO/BADGE | SmartphoneKey green logo mark |
| `68ed0d890ec468824c776ef1_Security Shield Icon White.I01.2k 2.webp` | 1080x1014 | 63.4 | - | - | not referenced | ILLUSTRATION | 3D padlock-in-shield icon, grey |
| `68ed0b8f9d07780e2cebdd5c_android-chrome-512x512.png` | 256x256 | 15.0 | - | - | 34 old pages | LOGO/BADGE | Logo mark (android-chrome icon) |
| `68ed0a9bf9f03729de948b75_favicon-32x32.png` | 32x32 | 2.9 | - | - | 34 old pages | LOGO/BADGE | Favicon 32x32 |
| `68ed090ed6b76cc1ec21759a_Frame 57.webp` | 484x484 | 28.4 | - | - | facility-services, referral-program, smart-home-integrators | DEVICE RENDER | Phone held to a transparent-edged wall unit with KEY logo (render/composite) |
| `68e925419774ec46b98395a4_1440х1080_ICP 2_ Airbnb hosts (8).webp` | 1080x1106 | 91.3 | - | - | index, smart-home-integrators | PHONE MOCKUP | Phone with "SmartphoneKey Bot" chat |
| `68e91eb2a5ec19a80b927bba_1440х1080_ICP 2_ Airbnb hosts (7).webp` | 1080x1106 | 113.4 | - | - | 4 old pages | PHONE MOCKUP | Hands holding a phone showing a camera feed |
| `68e91e72f2e6d57f5b75dc59_1440х1080_ICP 2_ Airbnb hosts (6).webp` | 1080x1106 | 112.5 | - | - | features | ILLUSTRATION | 3D cell tower icon |
| `68e91e1e3dfe79aebb27d2b6_1440х1080_ICP 2_ Airbnb hosts (5).webp` | 1080x1106 | 126.8 | - | - | features, index, security-professionals | DEVICE RENDER | Phone held to a wall unit with KEY logo (render/composite) |
| `68e91de99f1ace81e2e05e8b_1440х1080_ICP 2_ Airbnb hosts (4).webp` | 1080x1106 | 86.9 | - | - | not referenced | PHONE MOCKUP | Phone lock screen "Megan sent you a temporary key" |
| `68e91d21e4c53f52eeb2cc96_1440х1080_ICP 2_ Airbnb hosts (3).webp` | 1080x1106 | 80.4 | - | - | facility-services, features, index | ILLUSTRATION | QR code on a dark panel |
| `68e91bea2828a2d4a52b91df_Frame 1171276647.webp` | 2880x1496 | 23.1 | - | - | not referenced | DECOR | Dark gradient, wide |
| `68e917d5f2b132f71e790ef9_Frame 1171276657.webp` | 1080x1014 | 71.3 | - | - | how-it-works | DEVICE RENDER | Product box/unit render with "Scan to call" QR; the site's current reader image (`reader-800.webp`) is a resize of this file |
| `68e9179b4439d143e66bcefd_Frame 1171276646 (1).webp` | 2844x1454 | 17.3 | - | - | not referenced | DECOR | Dark gradient, wide |
| `68e9170f223cd923bf60399a_8.webp` | 1080x1014 | 50.8 | - | - | not referenced | DEVICE RENDER | Product box/unit render |
| `68e916d67218eeea6fe271cc_8.png` | 1080x1014 | 362.9 | - | - | not referenced | DEVICE RENDER | Product box/unit render (PNG) |
| `68e7c58e90b06955d9b7ddf1_1440х1080_ICP 2_ Airbnb hosts (2).webp` | 1080x1106 | 67.4 | - | - | features, index | PHONE MOCKUP | Phone Wallet screen mockup |
| `68e669c6b0bde8c64dac983b_Frame 1171276652.webp` | 2859x1394 | 11.9 | - | - | not referenced | DECOR | Dark gradient, wide |
| `68e6685c79b18a7a0ad3d93b_Frame 48.webp` | 2880x1542 | 11.1 | - | - | not referenced | DECOR | Dark gradient, wide |
| `68e6407ceffc8eddbaf07ee4_1440х1080_ICP 2_ Airbnb hosts (1) (1).webp` | 1080x928 | 22.8 | - | smartphone keys | 4 old pages | DEVICE RENDER | Product set render: wall unit, key tag, unlock-button unit, on grey |
| `68e52b5dcdfcd15a6dd248f7_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x928 | 23.8 | - | smartphone keys | index | PHONE MOCKUP | Hand holding a phone with an unlock icon over green |
| `68e50a6c05cc862269cb78fd_ad222843ac6e481ebca33b68ea1d85c2.mp4.webp` | 2880x1496 | 24.2 | - | - | not referenced | VIDEO POSTER | Poster of `ad222843...mp4`: woman at a door, grey |
| `68d3da6c9b53903c97b94645_Frame 56(1).png` | 363x363 | 108.8 | - | - | referral-program | PHONE MOCKUP | Phone with "SmartphoneKey Bot" chat |
| `68d3da6c0d8f37be41b73635_Frame 56(2).png` | 363x363 | 107.5 | - | - | referral-program, smart-home-integrators | PHONE MOCKUP | Phone Wallet screen mockup, white screen |
| `68d3da6c6d7a5300892d8b06_Frame 56(3).png` | 363x363 | 99.1 | - | - | referral-program | ILLUSTRATION | Chat bubble illustration |
| `68d3d95a6e0905bb2b0380c3_Frame 56.png` | 363x363 | 132.3 | - | - | not referenced | DEVICE RENDER | Hand holding a card ("Add me to wallet") toward a unit with QR |
| `68d288debd2d9804858a53b4_1440х1080_ICP 2_ Airbnb hosts.webp` | 1080x1024 | 377.1 | - | - | not referenced | DEVICE RENDER | Black KEY card with keyring on dark background |
| `68d278172170663a697bc17d_hero-img.webp` | 1080x1014 | 30.5 | - | - | referral-program | PHONE MOCKUP | Hero image: phone Wallet screen with Matter logo |

Raster flags: PHONE MOCKUP 20, ILLUSTRATION 17, DEVICE RENDER 12, DECOR 10, LOGO/BADGE 7, DOCUMENT 1, VIDEO POSTER 1. UI screenshots: 0. Reader photographs: 0 as still images (real reader footage exists only in the videos below and in the poster frame `69174a0a...poster.0000000.jpg`, which is a photograph of the reader on a yellow background).

Videos in `export/assets/files` (flag: VIDEO):

| File | Size / duration | Weight | Content (frames viewed every 4 s) |
|---|---|---|---|
| `69174a0a8b936895170fd3ce_option 1 - website vid.mp4` | 1920x1080, 25.6 s | 9.9 MB | **The product video** ("option 1 - website vid"): door scenes, reader render and photograph, a circuit-board photograph, two phone screens with SmartphoneKey splash/sign-in and App Store / Google Play badges (about 12 s), install and packaging scenes. Used on the old home page. |
| `68f7a58fb777c50817520602_1752714863844.mp4` | 1138x640, 43.2 s | 3.2 MB | Cleaning-crew case film: installed black wall reader, phone tap, elevator reader; shows a laptop log screen branded "ClearRight" (third-party-branded UI, not the Admin Panel). Not referenced by the mirrored pages. |
| `68f0c37412f4d702c4b51d93_ad222843ac6e481ebca33b68ea1d85c2.mp4` | 1920x1080, 33.3 s | 16.1 MB | Reader on walls, unboxing and installing the reader and unlock-button unit, phone Wallet tap, closing with text "Manage effortlessly with our Chatbot Admin Interface" over a woman using a phone; no Admin Panel screen. Not referenced by the mirrored pages. |
| `68d52e694771a4d60649764a_SmartphoneKey_website-video_1x1 (1).mp4` | 1080x1080, 20.9 s | 5.6 MB | "8 ways to use smartphone KEY": people at doors, titles (guest, Airbnb hosts, private spaces, businesses); no product UI. Used on the old `/referral-program`. |

Not tabulated: 52 SVG files (icons) and 4 documents (`6a723628e332dde9a55898d0_smartphonekey-ce-red-lte-reader-spk-ac-lte-eu-v1-0.pdf`, `6a723628bc718754327cf94c_smartphonekey-ce-red-wifi-reader-spk-ac-wifi-v1-0.pdf`, `6a72021ca74978a0c05b9c57_apple-ecp2-certification-confirmation.docx`, `692f090719ded7e2d4bc6b91_Instruction1112.pdf`).

### 3b. `mirror/site` raster images (png/jpg/webp)

150 image files under `mirror/site`, all below `site/_ext/cdn.prod.website-files.com/`: 72 originals and 78 Webflow responsive copies (`-p-500`, `-p-800`, `-p-1080`, `-p-1600`). Two Webflow project folders: `68d268370f87b6205f066fa5` (site assets) and `691486ca4fe3f4b24bc0e3e6` (CMS: blog covers and team portraits). Besides these, `mirror/site` holds 52 SVG, 2 MP4, 2 WebM, 3 PDF and 1 DOCX file. Filename-based flags: the `IMG_xxxx` names (IMG_3994, IMG_3906, IMG_1428_2, IMG_1432_2) look like camera files but the pictures are banner/cover graphics; `1440х1080_ICP 2_ Airbnb hosts (n)` and `Frame 1171276xxx` are design-tool exports (mockups, renders, illustrations); `Frame 5 (n)` are portraits; `box_visual_2`, `Card_3D_black`, `hero-img` are product renders. No filename suggests an Admin Panel or app screen.

| Path under `site/_ext/cdn.prod.website-files.com/` | Original | KB | Responsive copies (width: size) | Also in `export/assets` | Flag |
|---|---|---|---|---|---|
| `68d268370f87b6205f066fa5/68d278172170663a697bc17d_hero-img.webp` | 1080x1014 | 30.5 | - | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68d3da6c0d8f37be41b73635_Frame 56(2).png` | 363x363 | 107.5 | - | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68d3da6c6d7a5300892d8b06_Frame 56(3).png` | 363x363 | 99.1 | - | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68d3da6c9b53903c97b94645_Frame 56(1).png` | 363x363 | 108.8 | - | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68d52e694771a4d60649764a_SmartphoneKey_website-video_1x1 (1)-poster-00001.jpg` | 720x720 | 17.2 | - | yes | VIDEO POSTER |
| `68d268370f87b6205f066fa5/68e50a6c05cc862269cb78fd_ad222843ac6e481ebca33b68ea1d85c2.mp4.webp` | 2880x1496 | 24.2 | - | yes | VIDEO POSTER |
| `68d268370f87b6205f066fa5/68e52b5dcdfcd15a6dd248f7_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x928 | 23.8 | 500: 9.5 KB, 800: 17.0 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68e6407ceffc8eddbaf07ee4_1440х1080_ICP 2_ Airbnb hosts (1) (1).webp` | 1080x928 | 22.8 | 500: 9.4 KB, 800: 16.6 KB | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/68e6685c79b18a7a0ad3d93b_Frame 48.webp` | 2880x1542 | 11.1 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68e669c6b0bde8c64dac983b_Frame 1171276652.webp` | 2859x1394 | 11.9 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68e7c58e90b06955d9b7ddf1_1440х1080_ICP 2_ Airbnb hosts (2).webp` | 1080x1106 | 67.4 | 500: 20.1 KB, 800: 57.9 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68e9179b4439d143e66bcefd_Frame 1171276646 (1).webp` | 2844x1454 | 17.3 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68e917d5f2b132f71e790ef9_Frame 1171276657.webp` | 1080x1014 | 71.3 | 500: 14.0 KB, 800: 29.8 KB | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/68e91bea2828a2d4a52b91df_Frame 1171276647.webp` | 2880x1496 | 23.1 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68e91d21e4c53f52eeb2cc96_1440х1080_ICP 2_ Airbnb hosts (3).webp` | 1080x1106 | 80.4 | 500: 24.9 KB, 800: 76.5 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68e91e1e3dfe79aebb27d2b6_1440х1080_ICP 2_ Airbnb hosts (5).webp` | 1080x1106 | 126.8 | 500: 26.9 KB, 800: 75.5 KB | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/68e91e72f2e6d57f5b75dc59_1440х1080_ICP 2_ Airbnb hosts (6).webp` | 1080x1106 | 112.5 | 500: 28.9 KB, 800: 91.8 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68e91eb2a5ec19a80b927bba_1440х1080_ICP 2_ Airbnb hosts (7).webp` | 1080x1106 | 113.4 | 500: 25.1 KB, 800: 67.0 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68e925419774ec46b98395a4_1440х1080_ICP 2_ Airbnb hosts (8).webp` | 1080x1106 | 91.3 | 500: 19.2 KB, 800: 50.0 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68ed090ed6b76cc1ec21759a_Frame 57.webp` | 484x484 | 28.4 | - | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/68ed0a9bf9f03729de948b75_favicon-32x32.png` | 32x32 | 2.9 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/68ed0b8f9d07780e2cebdd5c_android-chrome-512x512.png` | 256x256 | 15.0 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/68ee5644741cd6f949c2c684_Frame 48.png` | 2880x1418 | 2201.9 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68ef3801e6623f8e7cb27ed7_2.webp` | 2280x388 | 22.9 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68f0f69453c833bb6233453f_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x1106 | 64.6 | 500: 19.5 KB, 800: 54.7 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68f102be655bdd0c45b475fe_Group 44332.webp` | 2418x1502 | 773.5 | - | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68f105854552b5450ca85721_1440х1080_ICP 2_ Airbnb hosts (2).webp` | 1080x1066 | 22.3 | 500: 9.5 KB, 800: 16.5 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68f105ce9ab52dc805b3637e_Frame 57 (1).webp` | 484x484 | 23.1 | - | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68f24399ecdae67d56a919b3_2.jpg` | 345x259 | 31.2 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68f25476d4161cc0ba01790a_Frame 1171276723 (1).webp` | 1080x1014 | 72.3 | 500: 22.1 KB, 800: 48.8 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68f261d2adf9ba48cb72182f_Frame 1171276759.png` | 375x852 | 55.2 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68f262f2d6d79fa921b10a54_Group 44334 (1).png` | 375x441 | 209.6 | - | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68f263b70127c72dedc41688_Ellipse 1.png` | 375x486 | 173.7 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/68f8a42fb1318c82dfed8ff7_Security Shield Icon White.I01.2k 2 (1).png` | 1080x1014 | 350.5 | 500: 47.2 KB, 800: 121.5 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68fa0a6ba962874da8b29d31_1440х1080_ICP 2_ Airbnb hosts (3).webp` | 1080x1106 | 420.0 | 500: 9.3 KB, 800: 16.0 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68fa0a709e52acc3f4872863_1440х1080_ICP 2_ Airbnb hosts.webp` | 1080x1106 | 61.9 | 500: 23.2 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68fa0a737b5d3a8cd1169299_1440х1080_ICP 2_ Airbnb hosts (1).webp` | 1080x1106 | 64.6 | 500: 19.5 KB, 800: 54.7 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68fa0a772030ba1891c6727d_1440х1080_ICP 2_ Airbnb hosts (2) (1).webp` | 1080x1106 | 77.3 | 500: 27.2 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68fa0d05627b1e922d5d6dbd_Frame 1171276658.webp` | 540x507 | 66.0 | 500: 55.7 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68fa0dc6c749456b59200156_1440х1080_ICP 2_ Airbnb hosts (3) (1).webp` | 1080x1106 | 78.9 | 500: 28.7 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68fa0df1491940172d8dc341_1440х1080_ICP 2_ Airbnb hosts (4).webp` | 1080x1106 | 57.9 | 500: 17.2 KB, 800: 45.5 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/68fa0e312b1770e357d3dccf_1440х1080_ICP 2_ Airbnb hosts (5).webp` | 1080x1106 | 68.0 | 500: 21.7 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/68ffa3b03dbf94ecd0722881_Frame 1171276647.webp` | 2880x846 | 7.8 | - | yes | DECOR |
| `68d268370f87b6205f066fa5/69036e89b74ee938a6655e65_1440х1080_ICP 2_ Airbnb hosts (1).jpg` | 808x438 | 184.2 | 500: 13.6 KB, 800: 28.5 KB | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/690384cef00866500f84b14d_1440х1080_ICP 2_ Airbnb hosts (2).jpg` | 808x438 | 244.0 | 500: 14.2 KB, 800: 27.7 KB | yes | DEVICE RENDER |
| `68d268370f87b6205f066fa5/6903855c7b67e7811dc4bd99_1440х1080_ICP 2_ Airbnb hosts (3).jpg` | 808x438 | 143.1 | 500: 9.7 KB, 800: 18.8 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/69038ee2adc81b5161ee33c9_1440х1080_ICP 2_ Airbnb hosts (4).jpg` | 808x438 | 139.9 | 500: 10.1 KB, 800: 18.8 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/69038f22c51647ed105d8f2c_1440х1080_ICP 2_ Airbnb hosts (5).jpg` | 808x438 | 135.4 | 500: 9.4 KB, 800: 17.2 KB | yes | PHONE MOCKUP |
| `68d268370f87b6205f066fa5/69038f5bcc8afa0a6c149032_1440х1080_ICP 2_ Airbnb hosts (6).jpg` | 808x438 | 148.8 | 500: 12.1 KB, 800: 21.6 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/69038f9fdb70dd13365ef8f8_1440х1080_ICP 2_ Airbnb hosts (7).jpg` | 808x438 | 147.1 | 500: 7.9 KB, 800: 14.3 KB | yes | ILLUSTRATION |
| `68d268370f87b6205f066fa5/69174a0a8b936895170fd3ce_option 1 - website vid_poster.0000000.jpg` | 1280x720 | 23.7 | - | yes | VIDEO POSTER |
| `68d268370f87b6205f066fa5/6a16f8062d8f5c730d20102c_Google Play Badge.png` | 646x250 | 4.8 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/6a16f83971435c1aee26c09c_ChatGPT Logo.png` | 480x480 | 21.4 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/6a16fd0c390d07357cde5b7d_Google Play Icon.png` | 480x480 | 10.6 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/6a16fd0eb1e4c275dd0bdac7_App Store Icon.png` | 480x480 | 10.3 | - | yes | LOGO/BADGE |
| `68d268370f87b6205f066fa5/6a72021c4de7e87a0f7f39bd_google-smarttap-2-1-compliance-certificate.jpeg` | 801x993 | 69.0 | - | yes | DOCUMENT |
| `691486ca4fe3f4b24bc0e3e6/691487c5e3f1f6b2cacca44c_1440х1080_ICP 2_ Airbnb hosts.jpg` | 1616x876 | 493.1 | 500: 13.0 KB, 800: 26.9 KB, 1080: 41.3 KB, 1600: 69.1 KB | mirror only | PHONE MOCKUP |
| `691486ca4fe3f4b24bc0e3e6/6915fb2b2c7827813ff7044a_box_visual_2.webp` | 1100x619 | 38.6 | 500: 9.3 KB, 800: 17.4 KB, 1080: 24.7 KB | mirror only | DEVICE RENDER |
| `691486ca4fe3f4b24bc0e3e6/6915fc05b1a9c5eb802f7cf5_IMG_3994.webp` | 1100x619 | 51.2 | 500: 14.4 KB, 800: 25.5 KB, 1080: 34.3 KB | mirror only | BANNER |
| `691486ca4fe3f4b24bc0e3e6/6915fc7c6ae3255ac2f119fb_IMG_3906.webp` | 1100x451 | 22.9 | 500: 5.6 KB, 800: 10.1 KB, 1080: 14.7 KB | mirror only | DEVICE RENDER |
| `691486ca4fe3f4b24bc0e3e6/6915fcc4480fdb0f04c95f1d_Card_3D_black.webp` | 1100x619 | 33.8 | 500: 9.2 KB, 800: 16.3 KB, 1080: 23.4 KB | mirror only | DEVICE RENDER |
| `691486ca4fe3f4b24bc0e3e6/6915fd8fcb78ff2fd8c8154e_IMG_1428_2.webp` | 992x558 | 39.9 | 500: 11.3 KB, 800: 19.1 KB | mirror only | BANNER |
| `691486ca4fe3f4b24bc0e3e6/69174c61f12fefafb8fa18d7_Frame 5.png` | 720x778 | 517.2 | 500: 87.3 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174ca3a20508978372e810_Frame 5 (1).png` | 720x778 | 557.9 | 500: 90.1 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174d4f3ebbf3e41e56e1ce_Frame 5 (2).png` | 720x778 | 626.9 | 500: 99.9 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174e0c92053ca1b677c45a_Frame 5 (3).png` | 720x778 | 452.7 | 500: 107.3 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174e8512e1d742686343c1_Frame 5 (4).png` | 720x778 | 554.6 | 500: 108.2 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174eabc9fb21d228595267_Frame 5 (5).png` | 720x778 | 522.9 | 500: 83.4 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174f10365674cafc47f7ad_Frame 5 (7).png` | 720x778 | 566.5 | 500: 95.7 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174f2c94da5997d2e4e313_Frame 5 (8).png` | 720x778 | 535.0 | 500: 91.6 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/69174f9e3e46a7ddad46749c_Frame 5 (9).png` | 720x778 | 471.7 | 500: 80.8 KB | mirror only | PORTRAIT |
| `691486ca4fe3f4b24bc0e3e6/691db34261fb42f26b50bb7c_IMG_1432_2.webp` | 1000x562 | 37.5 | - | mirror only | BANNER |

Flags over the 72 originals: PHONE MOCKUP 18, ILLUSTRATION 13, DECOR 10, DEVICE RENDER 9, PORTRAIT 9, LOGO/BADGE 6, VIDEO POSTER 3, BANNER 3, DOCUMENT 1.

### 3c. `implementation/addons/spk_website_v2/static/src/img` (current addon)

| File | Dimensions | KB |
|---|---|---|
| `img/apple-touch-icon.png` | 180x180 | 33.8 |
| `img/brand-mark.png` | 123x120 | 14.0 |
| `img/favicon-32.png` | 32x32 | 2.9 |
| `img/og-default.png` | 1200x630 | 128.6 |
| `img/reader-480.webp` | 480x451 | 15.3 |
| `img/reader-800.webp` | 800x751 | 33.6 |
| `img/posts/691487c5e3f1f6b2cacca44c.webp` | 1200x650 | 20.0 |
| `img/posts/6915fb2b2c7827813ff7044a.webp` | 1100x619 | 28.9 |
| `img/posts/6915fc05b1a9c5eb802f7cf5.webp` | 1100x619 | 37.7 |
| `img/posts/6915fc7c6ae3255ac2f119fb.webp` | 1100x451 | 17.2 |
| `img/posts/6915fcc4480fdb0f04c95f1d.webp` | 1100x619 | 27.1 |
| `img/posts/6915fd8fcb78ff2fd8c8154e.webp` | 992x558 | 27.7 |
| `img/posts/691db34261fb42f26b50bb7c.webp` | 1000x562 | 27.7 |
| `img/team/alex-sydorenko.webp` | 480x519 | 13.3 |
| `img/team/denys-merkulov.webp` | 480x519 | 11.8 |
| `img/team/ioannis-mavridis.webp` | 480x519 | 11.0 |
| `img/team/kate-vasylenko.webp` | 480x519 | 12.8 |
| `img/team/kostiantyn-dolzhenko.webp` | 480x519 | 10.7 |
| `img/team/lana-ostapenko.webp` | 480x519 | 10.8 |
| `img/team/oleksii-andrieiev.webp` | 480x519 | 15.1 |
| `img/team/vadym-sydorenko.webp` | 480x519 | 9.8 |
| `img/team/vitalii-dolzhenko.webp` | 480x519 | 14.2 |

The reader image (`reader-480.webp`, `reader-800.webp`) is the resized product render `68e917d5...Frame 1171276657.webp` (Used on the old `/how-it-works` with empty alt; the addon alt is "SmartphoneKey reader from the current product image library"). `og-default.png` alt in `site_content.py`: "SmartphoneKey reader beside the SmartphoneKey key logo". Posts and team images are copies of the CMS images. Also in `static/src`: `files/google-smart-tap-2-1-compliance-certificate.jpeg` (801x993, 69.0 KB), `files/*.pdf` (2), `files/*.docx` (1), and, untracked in the working tree, `fonts/manrope-*.woff2` (Manrope variable, latin, latin-ext, cyrillic, cyrillic-ext).

### 3d. Public instruction pages (read-only GET)

| URL | HTTP status | `<title>` | `<img>` count | Images |
|---|---|---|---|---|
| `spkey.odoo.com/instructions/admin-panel` | 200 | SmartphoneKey · Admin Panel Walkthrough | 0 | none |
| `spkey.odoo.com/instructions/admin-guide` | 200 | SmartphoneKey · Admin Portal User Guide | 0 | none |
| `spkey.odoo.com/instructions/mobile-app` | 200 | SmartphoneKey · Mobile App Walkthrough | 0 | none |
| `spkey.odoo.com/guide-for-usage-and-installation` | 200 | SmartphoneKey · Physical Connection & Specifications | 8 | see below |

No redirects, no login wall; all four answered 200 without cookies.

**`/guide-for-usage-and-installation`: 8 `<img>` tags** (plain `src`, no lazy-load attributes; paths relative to `https://spkey.odoo.com`):

| src | alt | Looks like |
|---|---|---|
| `/smartphonekey/static/src/img/instruction_site/reader.png` | 'Reader with backplate' | Reader product image on grey (studio shot; photo or render cannot be told from the file; 3000x4000 in the addon repo, see 3f) |
| `/smartphonekey/static/src/img/instruction_site/exit-button.png` | 'Exit button with backplate' | Exit-button unit product image (2768x3704 in the addon repo) |
| `/smartphonekey/static/src/img/instruction_site/reader.png` | 'SmartphoneKey reader' | Reader product image on grey (studio shot; photo or render cannot be told from the file; 3000x4000 in the addon repo, see 3f) |
| `/smartphonekey/static/src/img/instruction_site/sim.png` | 'SIM installation — unscrew, insert, close, tighten.' | SIM installation drawing (line diagram, 1400x720) |
| `/smartphonekey/static/src/img/instruction_site/wiring-maglock.jpg` | 'Maglock — full wiring diagram.' | Wiring diagram (JPEG; per its alt text) |
| `/smartphonekey/static/src/img/instruction_site/wiring-strike.jpg` | 'Electric strike — full wiring diagram.' | Wiring diagram (JPEG; per its alt text) |
| `/smartphonekey/static/src/img/instruction_site/sim.png` | 'The SIM holder sits under the back cover — Step 4 walks you through it.' | SIM installation drawing (line diagram, 1400x720) |
| `(empty)` | '' | empty placeholder (src and alt empty) |

Distinct image files on that page: `reader.png` (used twice), `exit-button.png`, `sim.png` (used twice), `wiring-maglock.jpg`, `wiring-strike.jpg`. None is an Admin Panel or app screen.

**`/instructions/admin-panel`, `/instructions/admin-guide`, `/instructions/mobile-app`: 0 `<img>` tags each.** Other image mechanisms on those pages (listed from the HTML, images not downloaded):

* `/instructions/admin-panel` (11.9 KB HTML): an interactive walkthrough built by `/smartphonekey/static/src/js/admin_panel.js`. The page says "This is an interactive demo. Buttons simulate the real portal"; the script contains demo data (e.g. "Demo Admin", `demo.admin@example.com`). No image files. Not a screenshot.
* `/instructions/admin-guide` (223 KB HTML): 35 numbered sections and 59 `data-preview` hooks that open SVG previews: `keys.svg` (15), `users.svg` (12), `entities.svg` (7), `local-admins.svg` (5), `create-user.svg` (5), `lock-access.svg` (4), `dashboard.svg` (4), `registration-page.svg` (3), `entity-selector.svg` (2), `sign-in.svg` (1), `create-entity.svg` (1): 11 distinct files under `/smartphonekey/static/src/img/instruction_site/guide/`. The SVG files are 1.3 to 6.4 KB each (checked in the sibling repo, 3f): hand-written vector sketches of portal screens (window dots, boxes, text elements), not screenshots.
* `/instructions/mobile-app` (32 KB HTML): an interactive iPhone mock built by `mobile_app.js` from an embedded JSON (`#mobile-app-data`) that lists 13 scene images under `/smartphonekey/static/src/img/instruction_site/mobile/`: `call-history.png`, `camera-live.png`, `devices-grid.png`, `home-empty.png`, `home-overview.png`, `intro.png`, `key-actions.png`, `key-concierge.png`, `key-temporary.png`, `keys-list.png`, `profile-account.png`, `profile-menu.png`, `sign-in.png`. These are the closest thing to app screens; see 3f for what they are.

### 3e. Old site typography (`mirror/raw/index.html`, `mirror/site` CSS)

The old Webflow site loads Google Fonts through the Web Font Loader (`ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js`) with `WebFont.load({google:{families:["Inter:300,400,500,600,700","Poppins:300,400,500,600,700","Roboto:300,400,500,600,700"]}})`; the same call is on all 34 raw pages. There are no `<link>` tags to `fonts.googleapis.com` (only `preconnect` to it and to `fonts.gstatic.com`) and no `@font-face` other than the Webflow icon font.

| Family | Weights loaded | Where it is actually declared |
|---|---|---|
| **Poppins** | 300, 400, 500, 600, 700 | `<body class="site-body-main">` on 29 of the 34 raw pages (`font-family: Poppins, sans-serif; font-size: 1.111vw; line-height: 136%; color #000000b3`), `.site-body` (18px, weight 400) on the body of `referral-program`, `.cert-page`; inline page CSS: `.page-content-innser` body text weight 400 (1.125em/155.6%) on the posts, `.note-field a` weight 500 on the team pages. Main marketing and body font. |
| **Inter** | 300, 400, 500, 600, 700 | Article headings: `.page-content-innser h2` (1.667em/120%, weight 600) and `h3` (1.333em/150%, weight 600) in the post pages; `.ap-redirect` in the shared CSS. |
| Roboto | 300, 400, 500, 600, 700 | Requested by the loader but no `font-family: Roboto` rule exists in the shared CSS or in the inline CSS of the 34 raw pages. |
| Arial, sans-serif | - | Default `body` rule of the Webflow shared CSS (14px/20px); applies where no class sets a family: the plain `<body>` of `404`, `adminpanel`, `apps-and-chatbot` and `products/smartphonekey-reader-1`. |

Weights declared in the shared CSS (`css/smartphonekey-ec24fb.webflow.shared.c1bb3e5cb.css`, 107 KB): 600 (35 rules), 500 (28), 700 (15), 400 (5 plus 6 `normal` and 4 `bold`), 300 (2). Heading sizes in the base rules: h1 38px, h2 32px, h3 24px, h4 18px. For comparison, `static/src/fonts` (untracked in the working tree, files dated 12:01 today; not part of commit 45b3296) holds Manrope variable woff2 files (latin, latin-ext, cyrillic, cyrillic-ext) and the OFL licence.

### 3f. Reference: product images in the sibling repository (outside the workspace)

Found while checking where the instruction pages get their images; listed because they are the only app-screen and reader-photo files located. Read-only listing of `C:\Project\Development\spk-odoo-ap429\addons\smartphonekey\static\src\img` (files not copied or edited).

| File (`instruction_site/`) | Dimensions | KB | Looks like |
|---|---|---|---|
| `mobile/call-history.png` | 390x844 | 122.7 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/camera-live.png` | 812x375 | 467.0 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/devices-grid.png` | 780x1688 | 68.9 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/home-empty.png` | 780x1688 | 271.1 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/home-overview.png` | 780x2266 | 487.5 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/intro.png` | 390x844 | 16.9 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/key-actions.png` | 780x1688 | 109.4 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/key-concierge.png` | 780x1688 | 56.6 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/key-temporary.png` | 780x1688 | 121.3 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/keys-list.png` | 780x2184 | 126.9 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/profile-account.png` | 390x844 | 13.9 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/profile-menu.png` | 390x844 | 26.2 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `mobile/sign-in.png` | 390x844 | 22.0 | App screen image, portrait phone UI (landscape for `camera-live`), demo data such as "Back entrance" and "Virtual Concierge" |
| `exit-button.png` | 2768x3704 | 725.5 | Product image of the exit/unlock button unit, on grey |
| `reader.png` | 3000x4000 | 1037.7 | Product image of the black reader with KEY logo, on grey |
| `sim.png` | 1400x720 | 50.8 | SIM card installation line drawing |
| `wiring-maglock.jpg` | 1503x1047 | 73.4 | Wiring diagram |
| `wiring-strike.jpg` | 1503x1047 | 74.0 | Wiring diagram |
| `guide/create-entity.svg` | vector | 1.9 | Vector sketch of a portal screen |
| `guide/create-user.svg` | vector | 2.3 | Vector sketch of a portal screen |
| `guide/dashboard.svg` | vector | 3.8 | Vector sketch of a portal screen |
| `guide/delegate-role.svg` | vector | 2.5 | Vector sketch of a portal screen |
| `guide/entities.svg` | vector | 6.4 | Vector sketch of a portal screen |
| `guide/entity-selector.svg` | vector | 2.1 | Vector sketch of a portal screen |
| `guide/import-csv.svg` | vector | 2.2 | Vector sketch of a portal screen |
| `guide/keys.svg` | vector | 3.1 | Vector sketch of a portal screen |
| `guide/local-admins.svg` | vector | 2.9 | Vector sketch of a portal screen |
| `guide/lock-access.svg` | vector | 2.2 | Vector sketch of a portal screen |
| `guide/registration-page.svg` | vector | 1.6 | Vector sketch of a portal screen |
| `guide/sign-in.svg` | vector | 1.3 | Vector sketch of a portal screen |
| `guide/users.svg` | vector | 5.3 | Vector sketch of a portal screen |

Provenance as stated in that repository: `static/src/js/mobile_app.js` header says the walkthrough is built "from the design mock-ups" and that "The mock-ups predate the current app (AP-341) ... Refreshing the images needs new captures." `admin_panel.js` describes itself as "an interactive mock of the live SmartphoneKey Admin" with demo data. So the repository holds app images that are design mock-ups of an earlier app version, 13 Admin Portal vector sketches and one scripted Admin Panel mock, but no current device captures of either interface.

## 4. Routes by locale

Locales: EN (root), FR `/fr`, DE `/de`, ES `/es`, UK `/uk` (`SITE_LANGS`). **T** = page text translated into that language (own canonical URL and hreflang set, listed in the sitemap); **E** = English text, also reachable under the language prefix, canonical points to the English URL, no hreflang alternates, listed once in the sitemap. Rule sources: `ENGLISH_ONLY = ("/privacy-policy", "/terms-of-service")` in `site_content.py`; `SpkWebsiteV2Legacy.post` and `.team_member` pass `english_only=True` in `controllers/main.py`; `implementation/registers/routes.json` ("English-only in every language (canonical = English URL): /privacy-policy, /terms-of-service, /post/*, /team/*"). Verified in `qa/sitemap-production-mode.xml`: 117 URLs = EN 37, FR 20, DE 20, ES 20, UK 20 (20 translated pages per language + 17 English-only pages). Automated tests cover this for `/platform`, the sitemap and three English-only samples (`test_i18n.py`); the other rows rest on the rule, not on a per-route test.

| Path | Type | EN | FR | DE | ES | UK | Sitemap URLs | Notes |
|---|---|---|---|---|---|---|---|---|
| `/` | page (new) | EN | T | T | T | T | 5 | page_home |
| `/platform` | page (new) | EN | T | T | T | T | 5 | page_platform |
| `/platform/access-management` | page (new) | EN | T | T | T | T | 5 | page_access_management |
| `/platform/automation` | page (new) | EN | T | T | T | T | 5 | page_automation |
| `/platform/visitor-access` | page (new) | EN | T | T | T | T | 5 | page_visitor_access |
| `/solutions/property-managers` | page (new) | EN | T | T | T | T | 5 | page_property_managers |
| `/solutions/integrators` | page (new) | EN | T | T | T | T | 5 | page_integrators |
| `/products/readers` | page (new) | EN | T | T | T | T | 5 | page_readers |
| `/compatibility` | page (new) | EN | T | T | T | T | 5 | page_compatibility |
| `/security` | page (new) | EN | T | T | T | T | 5 | page_security |
| `/resources` | page (new) | EN | T | T | T | T | 5 | page_resources |
| `/find-your-setup` | page (new) | EN | T | T | T | T | 5 | page_setup |
| `/contact` | page (new) | EN | T | T | T | T | 5 | page_contact |
| `/about` | page (new) | EN | T | T | T | T | 5 | page_about |
| `/thank-you` | page (new) | EN | T | T | T | T | 0 | page_thank_you; noindex, not in sitemap |
| `/certifications` | page (retained Webflow URL) | EN | T | T | T | T | 5 | page_certifications |
| `/apps-and-chatbot` | page (retained Webflow URL) | EN | T | T | T | T | 5 | page_apps |
| `/privacy-policy` | page (retained Webflow URL) | EN | E | E | E | E | 1 | page_privacy_policy; legal text kept English until a reviewed translation exists |
| `/terms-of-service` | page (retained Webflow URL) | EN | E | E | E | E | 1 | page_terms_of_service; legal text kept English until a reviewed translation exists |
| `/resources/lte-vs-wifi-access-control` | guide (`spk.website.resource`) | EN | T | T | T | T | 5 | template `page_article`; body and fields translated |
| `/resources/mifare-classic-desfire-ev3` | guide (`spk.website.resource`) | EN | T | T | T | T | 5 | template `page_article`; body and fields translated |
| `/resources/matter-thread-access-control` | guide (`spk.website.resource`) | EN | T | T | T | T | 5 | template `page_article`; body and fields translated |
| `/resources/access-control-when-offline` | guide (`spk.website.resource`) | EN | T | T | T | T | 5 | template `page_article`; body and fields translated |
| `/post/how-smartphonekey-enhances-security-for-your-property` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/post/matter-standard-the-key-to-a-seamless-smart-home` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/post/smart-home-trends-2025-the-future-of-secure-and-connected-living` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/post/smartphonekey-official-launch` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/post/the-future-of-keyless-entry-why-its-time-to-upgrade-to-smartphonekey` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/post/welcome-to-smartphonekey-your-affordable-access-to-a-keyless-future` | archived article | EN | E | E | E | E | 1 | English by design; archive note shown |
| `/team/alex-sydorenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/denys-merkulov` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/ioannis-mavridis` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/kate-vasylenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/kostiantyn-dolzhenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/lana-ostapenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/oleksii-andrieiev` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/vadym-sydorenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |
| `/team/vitalii-dolzhenko` | team page | EN | E | E | E | E | 1 | biography English; role (`job_title`) and photo alt translated, shown translated on `/about` |

Page counts: 19 routes in `ROUTES` (17 translated, 2 English-only; `/thank-you` is translated but noindex), 4 guides, 6 posts, 9 team pages.

Other paths (not translated by this addon):

| Path | Behaviour | Locale note |
|---|---|---|
| `/404` | real 404 page (`page_404`) | rendered by `render_not_found`, strings translated (T in all five) |
| `/adminpanel` | served by baseline module `spk_website`, unchanged | redirects to the portal entry (303 to `/my` in the QA run, `qa/legacy-routes.txt`) |
| `/blog` | 301 redirect to `/resources` | language-neutral; the target then serves T/E as in the table above |
| `/facility-services` | 301 redirect to `/solutions/property-managers` | language-neutral; the target then serves T/E as in the table above |
| `/features` | 301 redirect to `/platform` | language-neutral; the target then serves T/E as in the table above |
| `/guide-for-usage-and-installation` | served by module `smartphonekey` (instruction site) | own language handling, see below |
| `/how-it-works` | 301 redirect to `/platform` | language-neutral; the target then serves T/E as in the table above |
| `/intercom-solution` | 301 redirect to `/platform/visitor-access` | language-neutral; the target then serves T/E as in the table above |
| `/products/smartphonekey-reader-1` | 301 redirect to `/products/readers` | language-neutral; the target then serves T/E as in the table above |
| `/referral-program` | served by baseline module `spk_website`, unchanged | noindex, not linked from the 2.0 pages, not in the sitemap (200 in the QA run); carries prices and partner terms outside the claim register |
| `/security-professionals` | 301 redirect to `/solutions/integrators` | language-neutral; the target then serves T/E as in the table above |
| `/smart-home-integrators` | 301 redirect to `/solutions/integrators` | language-neutral; the target then serves T/E as in the table above |
| `/team` | 301 redirect to `/about` | language-neutral; the target then serves T/E as in the table above |
| `/instructions/admin-guide` | served by module `smartphonekey`: Admin Panel user guide | own language handling, see below |
| `/instructions/admin-panel` | served by module `smartphonekey`: Admin Panel walkthrough | own language handling, see below |
| `/instructions/mobile-app-guide` | served by module `smartphonekey`: Mobile app user guide | own language handling, see below |
| `/instructions/mobile-app` | served by module `smartphonekey`: Mobile app walkthrough | own language handling, see below |

The instruction site (`smartphonekey` module, 5 paths in `INSTRUCTION_PATHS`) is outside the five-locale set: its pages offer 10 languages in their own switcher (EN, UA, ES, EL, DE, FR, KO, JA, PL, PT); the sitemap lists the 5 English paths only when that module is installed (not installed in the 117-URL QA sitemap; `/guide-for-usage-and-installation` answered 404 there).

## 5. Tests that assert literal copy

Files: `implementation/addons/spk_website_v2/tests/test_enquiry.py`, `test_i18n.py`, `test_migration.py`, `test_publication.py`, `test_routes.py`, `test_seo.py` (`common.py` has none). "Lives in" is where the asserted text currently sits (`grep` of views, data, `site_content.py`, controllers, models). Changing a phrase in the left column needs the test (and, for msgids, the four `.po` files) updated.

| Test line | Assertion | Literal asserted | Lives in |
|---|---|---|---|
| test_routes.py:49 | assertIn on `/` text | `"Your key to access control."` | views/home.xml:15 (h1), views/layout.xml:134 |
| test_routes.py:49 | assertIn on `/` text | `"Start with Wi-Fi coverage at each reader location."` | site_content.py:447 (`HOME_CONNECTION_COPY["wifi"]`) |
| test_routes.py:50 | assertIn on `/platform` | `"SmartphoneKey is an access control management platform."` | views/platform.xml:98 |
| test_routes.py:51 | assertIn on `/products/readers` | `"LTE reader", "Wi-Fi reader"` | views/components.xml:13 (table header) and many others |
| test_routes.py:51 | assertIn on `/products/readers` | `"Cellular coverage and suitable SIM and service"` | views/components.xml:16 |
| test_routes.py:52 | assertIn on `/resources/lte-vs-wifi-access-control` | `"LTE reader"` | data/website_resources.xml:27, :32 |
| test_routes.py:52 | assertIn on `/resources/lte-vs-wifi-access-control` | `"Choose the connection that fits the site"` | data/website_resources.xml:46 |
| test_routes.py:53 | assertIn on `/compatibility` | `"MIFARE Classic", "MIFARE DESFire EV3"` | data/website_compatibility.xml (row names), views/products.xml |
| test_routes.py:54 | assertIn on `/find-your-setup` | `"Start by checking Wi-Fi coverage and network requirements"` | site_content.py:377 (`SETUP_CONNECTION_ADVICE["wifi"]`), views/setup.xml:108 |
| test_routes.py:55 | assertIn on `/contact` | `"Send enquiry"` | views/contact.xml:146 (button) |
| test_routes.py:55 | assertIn on `/contact` | `"info@smartphonekey.com"` | site_content.py:17, views/contact.xml:12, :155 |
| test_routes.py:68 | assertIn, setup result without JS | `"Discuss LTE coverage, SIM provisioning and the reader model for your installation."` | site_content.py:378 (`SETUP_CONNECTION_ADVICE["cellular"]`), views/setup.xml:112 |
| test_routes.py:69 | assertIn, setup result without JS | `"MIFARE Classic and MIFARE DESFire EV3"` | site_content.py:421-422 (`SETUP_RULES`, cards rule; contains "programming workflows") |
| test_routes.py:76 | assertIn, setup result with `site=partner` | `"Plan the installation, the customer handover"` | site_content.py:418 (`SETUP_RULES`, integrator rule) |
| test_routes.py:44 | assertNotIn in `/thank-you` h1 | `"has been received"` | absent when no enquiry; present in views/contact.xml:162, :191 |
| test_routes.py:107 | assertEqual h1 of the 404 page | `"This page is not here."` | views/company.xml:243 |
| test_seo.py:130 | assertIn on `/resources/access-control-when-offline` | `"It does not prove a person passed through or the door opened."` | data/website_resources.xml:182 |
| test_seo.py:131 | assertIn on the same page | `"A revocation made while a reader is offline is pending, not enforced."` | data/website_resources.xml:188 |
| test_seo.py:133 | assertIn on `/platform/visitor-access` | `"Confirm availability and the required setup with our team."` | views/platform.xml:281 |
| test_seo.py:137 | assertIn on `/products/readers` | `"Each SmartphoneKey reader can act as a Thread Border Router and as a router in the Thread mesh."` | views/products.xml:43 |
| test_seo.py:138 | assertNotIn on `/products/readers` | `"Do not assume every reader is a Border Router"` | absent everywhere (guards a removed sentence) |
| test_i18n.py:40-47 | assertEqual: h1 of `/{fr,de,es,uk}/platform` equals `.po` translation of this msgid | `"Bring access management into one clear system."` | views/platform.xml:10 (`heading`); changing it needs the constant and 4 `.po` msgids |
| test_i18n.py:96 | assertEqual: JSON error text for `/de/website/spk/enquiry` equals `de.po` | `"Enter your name, between 2 and 120 characters."` | site_content.py:574, controllers/enquiry.py:33, views/contact.xml:150 |
| test_i18n.py:108 | assertIn on `/fr/compatibility` meta line | `"octobre 2026"` | rendered from the compatibility `verified_at` dates (2026-10-26) in French |
| test_publication.py:22, :25 | assertIn / assertNotIn in `_public_rows("cards")` | `"MIFARE Classic" (row name)` | data/website_compatibility.xml:12 |
| test_publication.py:35 | assertIn on `/compatibility` body | `"Reviewed %d " (label before the date)` | views/products.xml:133 |
| test_publication.py:42 | assertNotIn on `/compatibility` | `b"Distance between readers"` | row hidden in data/website_compatibility.xml:134 (unpublished claim) |
| test_publication.py:44 | assertIn on `/compatibility` | `b"Reader Thread roles"` | data/website_compatibility.xml:122 |
| test_publication.py:45 | assertIn on `/compatibility` | `b"No separate firmware version is needed for either role."` | data/website_compatibility.xml:124 |
| test_publication.py:49 | assertNotIn on `/compatibility` | `b"P05", b"P07", b"evidence_ref", b"internal_source", b"AP-379"` | evidence references must not be rendered |
| test_enquiry.py:62 | assertEqual on lead name | `"Website — Project planning — Example Properties"` | models/crm_lead.py:118 + `ENQUIRY_TYPES["project"]` label (site_content.py:317) |
| test_enquiry.py:166 | assertEqual h1 of `/thank-you` after a submit | `"Your enquiry has been received."` | views/contact.xml:191 |
| test_enquiry.py:168 | assertEqual h1 of `/thank-you` without a submit | `"No enquiry to confirm."` | views/contact.xml:195 |

Pattern assertions that constrain every page's wording (`test_seo.py:17-28`, applied to the text of all routes, `/certifications` and `/apps-and-chatbot` at `test_seo.py:119-126`):

| Line | Pattern (case as in the test) | Meaning |
|---|---|---|
| test_seo.py:18 | `\b80\s?(m|metres|meters)\b` (ignore case) | a link distance |
| test_seo.py:19 | `\bEV1\b|\bEV2\b` | a DESFire generation other than EV3 |
| test_seo.py:20 | `\b(1K|4K|2K|8K)\b` | a card memory size |
| test_seo.py:21 | `any matter device|all matter devices|every matter device works` | universal Matter support |
| test_seo.py:22 | `unlimited|any complexity` | unlimited scenarios |
| test_seo.py:23 | `generally available|available now` | Concierge availability |
| test_seo.py:24 | `bank-grade|unhackable|uncopyable|non-copyable|fully compliant` | umbrella security claim |
| test_seo.py:25 | `(?<!no )automatic failover(?! is not)` | failover |
| test_seo.py:26 | `\$\s?\d|€\s?\d|£\s?\d|\bprice\b` | a price |
| test_seo.py:27 | `book a demo|request a demo` | a demo funnel |

Other copy-adjacent structural assertions a rewrite can trip: `test_routes.py:18` exactly one `h1` per page; `:21-22` unique `<title>` and meta description per route; `:27` more than 60 words in `<main>`; `:28` no "lorem", "TODO", "TBD", "placeholder" in `<main>` text; `:38` `<title>` equals `ROUTES[path]["title"]`; `:92` exactly 2 tables on `/certifications`; `test_seo.py:110-112` breadcrumb names equal the visible breadcrumb; `:115` article `headline` equals the h1; `test_i18n.py:66` an `english-only` paragraph on English-only pages; `test_migration.py:41` an `archive-note` paragraph on every post; `test_routes.py:62` a `/platform` link in the main nav. No test asserts the programmer wording of section 1.

## Summary of key findings

* Programmer phrases: 10 device-implying msgids; hits per language: EN 10 (14 source lines in 5 files), FR 10, DE 10, ES 10, UK 10 (40 in the .po files). 19 further generic "card programming" msgids name no device.
* Product evidence: no real Admin Panel or mobile-app screenshot exists in the workspace; the old-site images are phone mockups, device renders, illustrations and portraits, and real reader photographs appear only in 3 of the 4 videos and one video poster. The sibling repo `spk-odoo-ap429` has 13 app-screen PNGs described in its code as pre-release design mock-ups, 13 Admin Portal SVG sketches and studio images of the reader and exit button.
* Old site font: Poppins (body, via `site-body-main`), Inter (article headings), Roboto loaded but never declared, Arial fallback; weights 300 to 700 requested.
* Translatable public msgids: 795 (about 7,015 English words), identical in fr, de, es and uk; 331 msgids (6,970 words) are English-only on purpose (privacy, terms, 6 posts, 9 bios); 115 are backend terms; 1241 msgids in total.
* Routes: 19 `ROUTES` pages (17 translated in all five languages, privacy and terms English-only), 4 guides translated, 6 posts and 9 team pages English-only; 117 sitemap URLs.
* Tests: 33 literal copy assertions listed in section 5, plus the forbidden-wording regexes in `test_seo.py:18-27`; none mentions programmers.
