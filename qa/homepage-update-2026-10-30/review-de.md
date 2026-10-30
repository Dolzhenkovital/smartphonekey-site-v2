# German (de) editorial review, strings of 30 October 2026

**Summary:** The 93 German strings are accurate: every limitation survives, product names are exact, no forbidden content, and every "English interface" caption says "englische Oberfläche". Nothing blocks.
The main work is consistency with terms already live on the same pages (entziehen, ausstellen, übernommen, Mitarbeitende, Team vor Ort, Zutrittsmanagement) and a handful of calques ("Oberflächennachweis", "nicht impliziert", "Leser offline") that read as translated English.

**Counts:** reviewed 93 · blocking 0 · should-fix 14 · minor 9

Sources: `translations-2026-10-30.json` (de), `i18n/de.po` (PO-Revision-Date 2026-10-30 20:05, matches the rendered pages), rendered `/de`, `/de/platform`, `/de/platform/access-management`, `/de/products/readers`, `/de/platform/visitor-access` on 127.0.0.1:8069.

## Checked and clean

- Limitations: "unterstützt" / "wo das unterstützt wird" / "hängen von der Installation ab" / "keine erteilte Freigabe" / "kein Nachweis, dass eine Person durchgegangen ist" / "hängen von Ihren Berechtigungen und der Konfiguration des Standorts ab" / "werden für jedes Projekt bestätigt" all present; the failover sentence is the negative statement only.
- Product names: SmartphoneKey, Admin Panel, Apple Wallet, Google Wallet, MIFARE Classic, MIFARE DESFire EV3, Matter, Thread, LTE, Wi-Fi, ChatGPT, AI Concierge, AI Assistant unchanged in every string; UI labels (Dashboard, Give Access, Assign Key, Guest Key, Wallet Key, Devices) kept in English in captions and alt texts.
- Forbidden content: no distance, DESFire generation, memory size, "jedes Matter-Gerät", "unbegrenzt", "verfügbar" for AI Concierge, price, demo, "Programmiergerät", "sofort" or "übernimmt den Rest".
- Lengths: longest new heading 43 characters (H2 "Leser und Zutrittscontroller in einem Gerät"); no new button over four words. "Zutrittscontroller" and "Benachrichtigungen" (18 characters) exceed the 16-character compound guidance but are the established glossary terms; keep.
- Not on the five pages in either language (reviewed from the JSON only): "Ask us to review the site…", "Issue and revoke Wallet keys…".
- No mojibake; soft hyphens appear only in paragraph text.

## Blocking

None.

## Should-fix

| English msgid (short) | Current German | Proposed German | Reason |
|---|---|---|---|
| Access management for buildings (home eyebrow) | Zutrittsverwaltung für Gebäude | Zutrittsmanagement für Gebäude | Title, nav, breadcrumbs and 29 other occurrences on these pages say "Zutrittsmanagement"; one term, one translation |
| Explore access management (link to /platform/access-management) | Zutrittsverwaltung entdecken | Zutrittsmanagement entdecken | Link label must match the page it opens ("Zutrittsmanagement"); rule 4 |
| Give residents, staff and contractors access… (home hero) | Geben Sie Bewohnern, Personal und Dienstleistern Zutritt… | Geben Sie Bewohnern, Mitarbeitenden und Dienstleistern Zutritt… | "staff" is "Mitarbeitende" on /platform and /platform/access-management; "Personal" appears only here |
| Visitors scan the entrance QR code to reach a resident or the site team. | …um einen Bewohner oder das Standortteam zu erreichen. | …um einen Bewohner oder das Team vor Ort zu erreichen. | "site team" is "Team vor Ort" on /platform and /platform/visitor-access (4×) |
| Revoke their access and check that the readers have applied the change. | Widerrufen Sie den Zutritt und prüfen Sie, ob die Leser die Änderung übernommen haben. | Entziehen Sie den Zutritt und prüfen Sie, ob die Leser die Änderung übernommen haben. | "revoke" is "entziehen"/"Zutrittsentzug" on /platform/access-management (6×); "widerrufen" appears only in the new strings |
| Issue and revoke Wallet keys (Apple Wallet, Google Wallet)… | …im Admin Panel ausgeben und widerrufen. | …im Admin Panel ausstellen und entziehen. | "issue" is "ausstellen" (4× on the same pages), "revoke" is "entziehen" |
| `<step-title>`Issue`</span>` a key or card, with a validity period where supported | Ausgeben einen Schlüssel oder eine Karte… | Ausstellen einen Schlüssel oder eine Karte… | Same page says "stellt einen Schlüssel oder eine Karte aus"; one verb for "issue" |
| Sending a change is not the same as a reader applying it… A revocation waiting for an offline reader is not yet in effect there. | Eine Änderung zu senden ist nicht dasselbe, wie sie von einem Leser anwenden zu lassen. … Ein Widerruf, der auf einen Leser offline wartet, ist dort noch nicht wirksam. | Eine Änderung zu senden heißt nicht, dass der Leser sie schon übernommen hat. Das Admin Panel zeigt für jede Änderung, ob sie aussteht, vom Leser bestätigt wurde oder fehlgeschlagen ist, und welche Leser online, offline oder nicht verbunden sind. Steht ein Zutrittsentzug für einen Leser noch aus, weil dieser offline ist, gilt er dort noch nicht. | First sentence is a calque; "auf einen Leser offline wartet" is ungrammatical; "Widerruf" conflicts with "Zutrittsentzug"; "übernommen"/"gilt dort noch nicht" match the existing wording on /platform/access-management |
| Combine readers with a built-in access controller and LTE, Wi-Fi or supported Thread connectivity. | Kombinieren Sie Leser mit integriertem Zutrittscontroller mit LTE, Wi-Fi oder… | Kombinieren Sie Leser mit integriertem Zutrittscontroller und LTE, Wi-Fi oder unterstützter Thread-Anbindung. | Double "mit … mit" misreads as "controller with LTE" |
| Mesh coverage and the route to the internet… automatic failover is not implied. | …hängt von der Installation ab; ein automatisches Failover ist nicht impliziert. | …hängt von der Installation ab; das bedeutet kein automatisches Failover. | "nicht impliziert" is a calque; the readers FAQ on the same page already says "Das bedeutet keinen automatischen Failover." |
| Admin Panel Dashboard, English interface (close-up)… The figures are interface values from a test account… (2 msgids) | Die Zahlen sind Oberflächenwerte eines Testkontos, keine Kundenkennzahlen. | Die Zahlen sind Anzeigewerte eines Testkontos, keine Kundenkennzahlen. | "Oberflächenwerte" is not a German word in this sense; "Anzeigewerte" is |
| Devices page in the Admin Panel… Interface evidence of monitoring, not a network layout. | …Oberflächennachweis der Überwachung, kein Netzwerkplan. Englische Oberfläche. | …Zeigt die Überwachung in der Oberfläche; kein Netzwerkplan. Englische Oberfläche. | "Oberflächennachweis" is an invented compound; meaning (interface evidence, not a layout) kept |
| Device overview with filters for online, offline and not-connected readers (alt) | Geräteübersicht mit Filtern für Leser online, offline und nicht verbunden | Geräteübersicht mit Filtern für Leser, die online, offline oder nicht verbunden sind | Post-posed adjectives are not German word order |
| Guest Key form in Wallet Key mode… The dates are the form's defaults at capture time, not a completed grant. (+ the shorter caption and the alt with "Gültigkeitsdaten") | …Gültigkeitsdaten und Empfängerfeld… Die Daten sind die Vorgabewerte des Formulars zum Aufnahmezeitpunkt, keine erteilte Freigabe. | …Gültigkeitszeitraum und Empfängerfeld… Die Datumsangaben sind die Vorgabewerte des Formulars zum Zeitpunkt der Aufnahme, kein bereits erteilter Zutritt. | "Die Daten" reads as "the data", "Gültigkeitsdaten" as "validity data"; "Gültigkeitszeitraum" is the term used two lines above on the same page; the limitation stays and becomes clearer |
| Recent activity in the Dashboard (close-up). An event is a record of what the reader reported… | Ein Ereignis ist der Eintrag dessen, was der Leser gemeldet hat, kein Nachweis, dass eine Person durchgegangen ist. | Ein Ereignis ist ein Eintrag darüber, was der Leser gemeldet hat, kein Nachweis, dass eine Person die Tür passiert hat. | "der Eintrag dessen, was" is stilted; "die Tür passiert hat" is the idiomatic form of "passed through" |

## Minor

| English msgid (short) | Current German | Proposed German | Reason |
|---|---|---|---|
| Recent activity in the Dashboard. An event is a record, not proof… | …kein Nachweis, dass eine Person durchgegangen ist. | …kein Nachweis, dass eine Person die Tür passiert hat. | Align with the close-up caption above |
| Admin Panel Dashboard, English interface… (2 msgids); The AI Assistant is part of the Admin Panel | Dashboard des Admin Panel…; Teil des Admin Panel | Dashboard im Admin Panel…; keep "Teil des Admin Panel" | Genitive without -s looks like an error to German readers; "im Admin Panel" avoids it and matches the alt text "Dashboards im SmartphoneKey Admin Panel" |
| Changes for an offline reader remain pending until it reconnects and applies them.; Applied is not the same as sent | …bis er wieder verbunden ist und sie anwendet.; Angewendet ist nicht gleich gesendet | …und sie übernimmt.; Übernommen ist nicht gleich gesendet | "apply" is "übernehmen" everywhere else on these pages (3×) |
| Ways to enter, not a product screen. | Wege hinein, keine Produktansicht. | Zutrittswege, keine Produktansicht. | "Wege hinein" is unidiomatic; /platform uses "So gelangen Personen hinein" |
| Example connection layout | Beispiel für eine Verbindungsanordnung | Beispiel für die Anbindung der Leser | "Verbindungsanordnung" is not an established term |
| View the full screen | Den ganzen Bildschirm ansehen | Die ganze Ansicht öffnen | "ganzer Bildschirm" suggests full-screen mode, not the full screenshot |
| Power, compatible lock hardware and local wiring are still required. Network layout… | Netzaufbau und Abdeckung hängen von der Installation ab. | Netzwerkaufbau und Abdeckung hängen von der Installation ab. | "Netzwerk…" is the form used on these pages ("Netzwerkplan", "Netzwerkeinrichtung") |
| Offer Apple Wallet and Google Wallet keys on supported devices, alongside physical NFC cards. | Bieten Sie Schlüssel für Apple Wallet und Google Wallet auf unterstützten Geräten an, neben physischen NFC-Karten. | Bieten Sie neben physischen NFC-Karten Schlüssel für Apple Wallet und Google Wallet auf unterstützten Geräten an. | Trailing "neben…" after the separable verb reads as an afterthought |
| Manage access to one or many buildings… (meta description) | Zutritt zu einem oder vielen Gebäuden verwalten: … | Zutritt zu einem oder mehreren Gebäuden verwalten: … | "einem oder mehreren" is the idiom; snippet length (≈150) unchanged |

## Notes for the English (not fixed here)

- "Someone leaves" is rendered as "Jemand zieht aus oder scheidet aus", which spells out resident and staff cases; this matches the existing /platform line "auszieht oder ausscheidet" and adds no fact. Keep.
- "Help inside the Admin Panel" → "Hilfe direkt im Admin Panel" adds "direkt"; harmless emphasis, kept.
