# Independent review: SmartphoneKey website 2.0, Ukrainian, French, German and Spanish

Date: 27 October 2026. Reviewer: an independent agent that did not write the translations.
Instance: local Odoo 18 at http://127.0.0.1:8069 (preview mode), language prefixes /uk, /fr, /de, /es; English rendered for comparison.
Sources: `docs/site-v2/GLOSSARY.md`, `docs/site-v2/LOCALE-BRIEF.md`, `docs/site-v2/04-COPY-DECK-EN.md` (strings in the "Review corrections (revision 2.2)" table are not counted), and `implementation/addons/spk_website_v2/i18n/{uk,fr,de,es}.po`. No project file was changed. Odoo, Docker and module updates were not run.

## How the review was done

- **Pages:** the twelve requested pages in each language. Extras were read for serious problems only: automation, visitor access, security, about, certifications, apps, the LTE and Matter guides, 404, the privacy policy, one team page and one archived post.
- **Capture:** headless Chrome through puppeteer-core, with a fresh browser context per page, at 1280×800 and 390×844. For each page I captured the visible text, title and meta description, H1–H3 line counts, button line counts, clipped or overflowing elements, and table scroll regions. Extra captures: the header at 1280 and 1024, the open language menu at 1280, the open mobile menu at 390, and the contact form after an empty submit at 390. Preview mode, so nothing was sent.
- **Text comparison:** the visible text of every page lines up one-to-one with the English page (84 of 84 page pairs). Each translated line was read next to its English line.
- **Catalogue check:** every catalogue `msgstr` was compared automatically with what the page actually shows.
- **Screenshots:** in `implementation/qa/review-locales/`, named `<lang>-<page>-<1280|390>.jpg`. Also `<lang>-header-1280.jpg`, `<lang>-header-1024.jpg`, `<lang>-langmenu-1280.jpg`, `<lang>-mobilemenu-390.jpg` (plus `-full`) and `<lang>-contact-errors-390.jpg`. The German home page was captured again because the first 390 px capture loaded without CSS.
- **Who read what:** I read Ukrainian line by line. French, German and Spanish were read line by line by three parallel reviewer passes using the same method; I spot-checked their main findings against the page text and the catalogues and changed several severities.

Severity:
- **Blocking:** must not ship. A wrong or changed fact, a dropped limitation, forbidden content, or a wrong or misleading interface string.
- **Should fix:** fix before the owner review. A calque or unnatural wording in a heading, navigation, button or lead, a key term used inconsistently, or a heading of four or more lines.
- **Minor:** polish.

## Summary

| Language | Blocking | Should fix | Minor |
|---|---|---|---|
| Ukrainian (uk) | 1 (deployment, X1) | 4 | 25 |
| French (fr) | 1 (deployment, X1) | 7 | 20 |
| German (de) | 1 (deployment, X1) | 5 | 22 |
| Spanish (es) | 1 (deployment, X1) | 10 | 17 |

**The one Blocking issue in every language is not translation work.** The catalogues are largely correct, but the running database still serves the previous translations of the data records: the compatibility rows, the four guides (name, description, SEO title, direct answer and parts of the body), and the team page meta description. The old texts are back on screen with them:
- the C05 wording about a "compatible programming device / built-in programmer";
- "DESFire EV3" without "MIFARE";
- the offline guide lead without "not in effect until the reader confirms it";
- the calques the owner rejected: «ідентифікатори доступу», «робочий процес», «офлайн», "workflow", "flujo de trabajo".

After a reload, the Ukrainian catalogue reads naturally. It contains none of the owner's flagged calques, and its terms are consistent. Its remaining problems are one four-line H1, two four-line guide H2s, a few headings and phrases worth tightening, and polish.

---

## Cross-language findings

**X1 · Blocking · all four languages · compatibility, the four guides, /resources, team pages: the database does not show the catalogue.**
- **How it was measured:** I compared every catalogue entry with the rendered pages. These record strings differ from their `msgstr`: uk 58, fr 57, de 39, es 42. The guide bodies were partly updated: the body terms are mixed old and new.
- **Ukrainian examples** (rendered → catalogue):
  - /compatibility, MIFARE rows: «Програмування ідентифікаторів доступу через робочий процес в Admin Panel за допомогою сумісного пристрою для програмування SmartphoneKey, зокрема вбудованого програматора зчитувача, де він є.» → `uk.po`: «Програмується з Admin Panel на зчитувачі SmartphoneKey із підтримкою програмування.» This is a C05 violation.
  - /compatibility, DESFire conditions: «Задокументований процес називає DESFire EV3. …» It drops «Доступно в підтримуваних конфігураціях зчитувачів» and shortens the product name. → `uk.po`: «Доступно в підтримуваних конфігураціях зчитувачів. У документації названо лише MIFARE DESFire EV3; …»
  - /compatibility, NFC row: «Фізичні NFC-ключі … поряд із цифровими ідентифікаторами доступу» / «Для програмування нової картки потрібні підтримувані сімейство карток і пристрій для програмування.» This is C05. → «NFC-картки» / «Нову картку програмують на зчитувачі SmartphoneKey із підтримкою програмування; це має бути MIFARE Classic або MIFARE DESFire EV3.»
  - MIFARE guide lead: «Сумісний програматор або підтримуваний вбудований програматор зчитувача записує ідентифікатор доступу через робочий процес в Admin Panel.» This is C05. → «Адміністратор запускає програмування в Admin Panel, а потім прикладає картку до зчитувача SmartphoneKey із підтримкою програмування. …»
  - MIFARE guide `<title>`: «Програмування MIFARE Classic і DESFire EV3 | SmartphoneKey» → «Картки MIFARE Classic і MIFARE DESFire EV3 | SmartphoneKey».
  - MIFARE guide description: 176 characters with «ідентифікаторів доступу» → 154 characters in `uk.po`.
  - MIFARE guide body:
    - «Admin Panel пов'язує цей ідентифікатор доступу з людиною» → «пов'язує картку з людиною».
    - «Документ Посібник користувача Admin Panel — у ній описано кожен екран.» is broken grammar and uses the wrong term. → «Докладніше: Інструкція користувача Admin Panel — у ній описано кожен екран.»
  - Offline guide lead: «Розрізняйте локальний доступ і віддалені зміни. У задокументованому процесі керування … можуть чекати в черзі …». It does not say that a revocation is not in effect until confirmed. → «… тому скасування доступу, зроблене, поки зчитувач без зв'язку, не діє на ньому, доки зчитувач його не підтвердить. …»
  - Offline guide name, H1, title and links: «Що відбувається, коли зчитувач переходить в офлайн-режим?» and «Контроль доступу, коли зчитувач офлайн». The platform page link already says «втрачає зв'язок». → «Що відбувається, коли зчитувач втрачає зв'язок?» and «Контроль доступу, коли зчитувач без зв'язку | SmartphoneKey».
  - Offline guide body: «Що це означає для відкликання», «Статус з'єднання», «Операції, що очікують», «онлайн», and «не надсилайте … ідентифікатори доступу», which adds an item the English does not have. The catalogue has «скасування доступу», «Стан зв'язку», «Зміни, що очікують», «на зв'язку», and no added item.
  - Matter guide (extra page): the lead is «… те, що може робити робочий процес …» and drops the reader roles (C13). The H1 ends with a full stop: «Matter і Thread для контролю доступу.» The body has «робочі процеси» twice and «ревізію зчитувача».
  - LTE guide (extra page): the old lead has no decision rule, and the title is 71 characters. In `uk.po` the title is 64 characters and the lead is correct.
  - Revocation is shown as «відкликайте» and commissioning as «підключені» in the stale rows. Everywhere else, and in `uk.po`, they are «скасуйте» and «додані».
- **Team page meta description** (all four languages): «Profile of Alex Sydorenko, Директор зі штучного інтелекту, on the SmartphoneKey website.» Every catalogue translates this code string, but the running server has not loaded it.
- **French, German and Spanish** show the same symptoms: programming-device wording on /compatibility and in the MIFARE guide, "workflow" / "Workflow" / "flujo de trabajo", "DESFire EV3" in the MIFARE title, the old offline, LTE and Matter leads, and the guide H1s that end with a full stop. Details are in each language section.
- **Fix:** reload the translations with `-u spk_website_v2 --i18n-overwrite`, force an update of the `noupdate` data records (compatibility rows and resources), then restart. Re-run this comparison afterwards. In this instance the four guides and /compatibility currently contradict C05 in every language.

**X2 · German and Spanish Should fix, Ukrainian Minor · guides, /compatibility, /resources archive: date format.**
`rendering.py:123` hard-codes `format_date(value, format="d MMMM y", …)`. This produces:
- de «27 Oktober 2026», which needs «27. Oktober 2026»;
- es «27 octubre 2026», which needs «27 de octubre de 2026»;
- uk «27 жовтня 2026», while /certifications already shows «14 березня 2025 р.».

French «27 octobre 2026» is correct. Use the locale's long format (`format="long"`) or a per-language pattern. This is a template fix, not catalogue work.

**X3 · not counted · /platform/visitor-access step "Contact".** The step shares its msgid with the navigation label, so uk shows «Контакти / з мешканцем або службою об'єкта» and the other languages show the same pattern. This is the known revision 2.2 change ("Reach"). Give it its own msgid when 2.2 reaches the templates.

**X4 · no locale problem · layout.**
- No language has page-level horizontal scroll or clipped or overflowing text, at either width.
- At 390 px every comparison and compatibility table (640 px) scrolls inside its own 356 px region, as designed, and no cell overflows.
- The /products/readers H2 about Thread roles takes 3 lines at 1280 in every language, including English, so it comes from the column width.
- The header action fits on the main bar at 1280 and at 1024 in all four languages, on one line, with no overlap with the navigation:

  | Language | Header action | Width at 1280 | Width at 1024 |
  |---|---|---|---|
  | uk | Рекомендації для об'єкта | 221 px | 213 px |
  | fr | Recommandations de site | 220 px | 212 px |
  | de | Standortempfehlungen | 202 px | 194 px |
  | es | Recomendaciones para su sitio | 256 px | 248 px |

- **Mobile menu at 390:** complete in all four languages: four groups, the "Already using" actions, Site recommendations and the language list. It is a 676 px panel that scrolls over 1,201 px of content, the same as English.
- **Language menu:** every language name is shown in its own language, with the current one marked.

---

## Ukrainian (uk)

**Overall verdict.** `uk.po` follows the owner's examples:
- «Платформа керування доступом», «Об'єкти клієнтів», «Зчитувач і контролер доступу в одному пристрої», «Надавайте доступ під час заселення та скасовуйте після виїзду», «Розкажіть про об'єкти, якими ви керуєте», «Показати рекомендації».
- "ви" is used consistently, and tasks are in the imperative.
- The terms hold everywhere: об'єкт, зчитувач, контролер доступу, ключ у Wallet, NFC-картка, скасувати, очікує / підтверджена / не вдалася, адміністратор об'єкта, Інструкції vs Посібники, «Рекомендації для об'єкта» as the label with «Рекомендації для вашого об'єкта» as the H1.
- No forbidden content appears, and every limitation is kept, including «де це підтримується», «ще не діє», «підтверджують для кожного проєкту» and «залежить від».

The owner's flagged calques («ідентифікатори доступу», «робочий процес», «життєвий цикл», «відправна точка», «Інсталяції», «дозволи») do not occur anywhere in `uk.po`. They appear on screen only through X1.

### 1. Naturalness and idiom
- **UK-01 · Should fix · /solutions/integrators H1** — «Встановлюйте, передавайте й підтримуйте системи доступу». It is 55 characters, takes **4 lines at 390** (the only H1 in any language that does) and 3 at 1280 (`uk-integrators-390.jpg`). «передавайте» has no addressee, and «системи доступу» is not the usual term (системи контролю доступу). → «Монтаж, передача й підтримка систем доступу» (the lead already names the customer), or «Встановлюйте й супроводжуйте системи контролю доступу».
- **UK-02 · Should fix · home (Events item), /platform/access-management (Events section)** — «Історія дій і записи аудиту для кожного об'єкта.» / «Переглядайте історію дій і записи аудиту кожного об'єкта.» «записи аудиту» is a calque of "audit records". → «Журнал дій і аудиту для кожного об'єкта.» / «Переглядайте журнал дій і аудиту кожного об'єкта.»
- **UK-03 · Should fix · /products/readers next step (H2)** — «Сплануйте зчитувачі для своїх дверей». In Ukrainian you do not "plan readers". → «Підберіть зчитувачі для своїх дверей»
- **UK-04 · Minor · /platform/access-management H1** — «Визначайте, хто які двері може відчиняти» is colloquial. → «Визначайте, хто і які двері може відчиняти»
- **UK-05 · Minor · home, Ways to enter** — «Кожен користується тим, що надає об'єкт.» → «Кожен користується тим, що йому видали на об'єкті.»
- **UK-06 · Minor · home, Change access** — «Додавайте або прибирайте двері, коли змінюються потреби людини.» → «Додавайте або забирайте доступ до дверей, коли змінюються потреби людини.»
- **UK-07 · Minor · home strip, /platform diagram** — «… в одному пристрої, з LTE або Wi-Fi» / «… контролером доступу, з LTE або Wi-Fi». → «… з підключенням через LTE або Wi-Fi»
- **UK-08 · Minor · /platform, status section** — «Admin Panel показує, чи кожна зміна очікує, підтверджена зчитувачем або не вдалася.» The «чи … або» construction is off. → «Admin Panel показує стан кожної зміни: очікує, підтверджена зчитувачем або не вдалася.»
- **UK-09 · Minor · /platform, parts section** — «Хаби та підтримувані пристрої Matter додають сценарії для підключених пристроїв.» → «Хаби та підтримувані пристрої Matter дають змогу створювати сценарії.»
- **UK-10 · Minor · /solutions/property-managers, Every building** — «Переглядайте події та стан зчитувачів на кожному об'єкті і зміни, що досі очікують, та налаштовуйте сповіщення …» → «Переглядайте події та стан зчитувачів на кожному об'єкті, стежте за змінами, що ще очікують, і налаштовуйте сповіщення …»
- **UK-11 · Minor · /solutions/property-managers checklist** — «Картки, ключі у Wallet або і те, і те» → «Картки, ключі у Wallet або обидва варіанти»
- **UK-12 · Minor · /solutions/integrators, role section** — «Адміністратори клієнта самі керують своїми людьми, ключами й картками.» → «Адміністратори клієнта самі керують доступом своїх людей, ключами й картками.»
- **UK-13 · Minor · /products/readers, installation list** — «Сумісний замок і пристрої для виходу, якщо вони потрібні» → «Сумісний замок і, за потреби, кнопка виходу»
- **UK-14 · Minor · /compatibility next step** — «Попросіть про конкретну перевірку» → «Попросіть перевірити вашу модель»
- **UK-15 · Minor · /contact form** — «Деталі проєкту» → «Опис проєкту»
- **UK-16 · Minor · /contact aside** — «Спершу шукаєте відповіді?» → «Хочете спершу знайти відповіді самостійно?»
- **UK-17 · Minor · find-your-setup, installer rule** (`uk.po`; not shown with the tested parameters) — «… і те, хто підтримуватиме об'єкт після цього.» → «… і визначте, хто підтримуватиме об'єкт після цього.»
- **UK-18 · Minor · typography, site-wide** — the apostrophe is the ASCII «'» (об'єкт, зв'язок). → the typographic apostrophe «’» or «ʼ», with one replace in `uk.po`.

### 2. Terminology consistency
After the X1 reload, every key term is consistent across navigation, headings, the tool, the form, the guides and the metadata:

| English term | Ukrainian |
|---|---|
| site | об'єкт; "Entities" only once on /platform |
| reader | зчитувач |
| access controller | контролер доступу |
| Wallet key | ключ у Wallet |
| NFC card | NFC-картка |
| revoke | скасувати |
| pending / confirmed / failed | очікує / підтверджена (зчитувачем) / не вдалася |
| site administrator | адміністратор об'єкта |
| instructions vs guides | Інструкції vs Посібники |
| Site recommendations | Рекомендації для об'єкта (H1: Рекомендації для вашого об'єкта) |
| commissioned | доданий |
| offline | без зв'язку |
| property teams | Управителі нерухомості |
| installers and integrators | Монтажники та інтегратори |

Product names are untranslated and spelled correctly in `uk.po`. The inconsistencies visible now are all X1: «відкликати», «офлайн», «статус», «підключені пристрої», «Посібник користувача Admin Panel», «DESFire EV3».

- **UK-19 · Minor · /resources, /security, /certifications** — «Записи регуляторів» is a calque. → «Записи в реєстрах регуляторів»
- **UK-20 · Minor · /compatibility next step, MIFARE guide** — «Не надсилайте ключі, паролі чи секретні дані карток.» Here «ключі» reads as the site's digital keys; the English means cryptographic keys. → «Не надсилайте криптографічні ключі, паролі чи секретні дані карток.»

### 3. Semantic fidelity
Apart from X1, there are no added facts, no dropped limitations, no forbidden content, and nothing that implies a third-party programmer. The FAQ says «SmartphoneKey не підтримує стороннє обладнання для запису карток.»
- **UK-21 · Minor · /products/readers FAQ, /compatibility LTE row** — «Автоматичне перемикання на резерв не передбачено.» / «Автоматичне перемикання на Wi-Fi не передбачено.» "Not implied" became "not provided", a product statement the English does not make. → «Це не означає автоматичного перемикання на резерв.» / «Це не означає автоматичного перемикання на Wi-Fi.»
- **UK-22 · Minor · find-your-setup Recommendation, and "Both or not sure"** — «… якщо немає ні того, ні іншого, попросіть нас оцінити об'єкт.» The English is "if neither is reliable", not "if there is neither". → «… якщо жоден зв'язок не надійний, попросіть нас оцінити об'єкт.»

### 4. Interface strings
Checked and correct:
- the banner;
- breadcrumbs (Головна › …);
- the navigation and footer groups;
- the result labels «Ваші відповіді / Рекомендація / Чому / Що ще перевірити на місці / Посібники за вашими відповідями», «Змінити відповіді», «Показати рекомендації», «Почати спочатку», «Обговорити ці рекомендації»;
- the prefill note;
- the form labels with «(обов'язково)» / «(необов'язково)» and «Оберіть варіант»;
- the errors after an empty submit, «Будь ласка, перевірте виділені поля.» and «Введіть своє ім'я: від 2 до 120 символів.» (`uk-contact-errors-390.jpg`);
- the hidden status messages «Надсилання…», «Не вдалося надіслати ваш запит…», the conflict and preview messages, and «Ваш запит отримано.»;
- table captions and headers;
- the operation labels «Зчитування · Програмування · Керування · Підключення · Адміністрування»;
- 404, «На цій сторінці», «Джерела», «Пов'язані сторінки»;
- the store badges «Доступно в Google Play» and «Завантажте в App Store»;
- the language names.

At 390 px every button fits on one line. The widest is «Ознайомитися з платформою» at 278 px.

- **UK-23 · Minor · home tool button and noscript** — «Детальні рекомендації» is the only button without a verb. → «Показати всі рекомендації» (the noscript text then reads «… натисніть «Показати всі рекомендації».»)
- **UK-24 · Minor · /platform/access-management button** — «Читати інструкцію Admin Panel» → «Відкрити інструкцію до Admin Panel»
- **UK-25 · Minor · /compatibility and guides, meta line** — «Факти про продукт перевірено 27 жовтня 2026» → «Дані про продукт перевірено 27 жовтня 2026 р.» (the date part is X2)
- **UK-26 · Minor · English-only note** (privacy, team, post) — «Ця сторінка англійською мовою. Перевіреного перекладу немає.» → «Ця сторінка доступна лише англійською. Перевіреного перекладу немає.»
- **UK-27 · Minor · archived-article note** — «… дивіться на сторінках Як працює SmartphoneKey та Перевірити сумісність.» A button label is used as a page name. → «… на сторінках «Як працює SmartphoneKey» і «Сумісність».» This needs its own msgid; Spanish has the same problem.
- **UK-28 · Minor · team meta description** (`uk.po`, once X1 is fixed) — «Профіль: %(name)s, %(job)s, на вебсайті SmartphoneKey.» → «%(name)s, %(job)s: профіль на вебсайті SmartphoneKey.»

### 5. Layout in Ukrainian
Line counts are shown as 1280/390. The H1 budget holds everywhere except UK-01:

| Page | H1 | Largest H2 |
|---|---|---|
| home | 2/3 | 2/3 |
| integrators | **3/4** | 2/2 |
| MIFARE guide | 3/3 | **2/4** |
| offline guide (stale record H1) | 3/3 | 1/2 |
| readers | 2/3 | 3/3 (same as EN) |
| property-managers | 2/3 | 2/2 |
| all other pages | 2 or fewer at 1280, 3 or fewer at 390 | 2 or fewer at 1280, 3 or fewer at 390 |

- **UK-29 · Should fix · MIFARE guide H2s** (and the matching "On this page" links) — «Зчитування, програмування, надання доступу та використання картки» and «Чому інші покоління та обсяги пам'яті потребують підтвердження» each take 4 lines at 390 (`uk-guide-mifare-390.jpg`). → «Чотири окремі операції з карткою» and «Чому інші покоління й обсяги треба підтвердити».
- **Other layout checks:**
  - The preview banner takes 3 lines at 390.
  - The hero shows the H1, lead, button and link above the fold at both sizes (`uk-home-390.jpg`, `uk-home-1280.jpg`).
  - The setup result wraps «Wi-Fi-/зчитувач» at the hyphen, which is acceptable.

### 6. Metadata (uk)
- **Titles:** all twelve pages are 65 characters or fewer; the longest is integrators at 64.
- **Descriptions:** only the MIFARE guide is over 160 (176). That is X1: the catalogue value is 154.
- The titles read as search snippets, for example «Платформа керування доступом для нерухомості | SmartphoneKey» and «LTE- і Wi-Fi-зчитувачі для контролю доступу | SmartphoneKey».
- On the extra pages, the LTE guide title (71) is X1 (the catalogue value is 64).

(UK Should fix: UK-01, 02, 03, 29. Minor: UK-04 to UK-28.)

---

## French (fr)

- "vous" is used consistently.
- French typography is correct: no-break spaces before « : ? ! » and curly apostrophes.
- No limitation is dropped and no forbidden content appears in `fr.po`. The failover negation is kept: «Cela n’implique pas de basculement automatique.»
- The English-only note «Cette page est en anglais. Aucune traduction relue n’est disponible.» is present.

### 1. Naturalness and idiom
- **FR-01 · Should fix · /solutions/integrators H1** — «Installez, remettez et assurez le support des systèmes d’accès» (62 characters; 3 lines at 1280 and at 390). «remettez» has no object, and «assurer le support» is an anglicism. → «Installation, remise au client et suivi des systèmes d’accès». Also change the step «Assurer le support» to «Suivi» and the H2 «De l’évaluation au support» to «De l’étude du site au suivi».
- **FR-02 · Should fix · /contact H1** — «Dites-nous ce que vous voulez résoudre» → «Décrivez votre besoin»
- **FR-03 · Should fix · /compatibility #cards** — «Un nom de famille ne couvre ni toutes les tailles de mémoire …» «nom de famille» means a person's surname. → «Le nom d’une famille de cartes ne couvre ni toutes les tailles de mémoire, ni tous les formats de données, ni les cartes d’un autre fournisseur.»
- **FR-04 · Minor · footer brand line** — «Votre clé du contrôle d’accès.» → «La clé de votre contrôle d’accès.»
- **FR-05 · Minor · home H2** — «Voyez ce qui s’est passé …» → «Suivez ce qui s’est passé et ce qui demande votre attention»
- **FR-06 · Minor · home, property-managers** — «Laissez un administrateur local gérer …» → «Confiez à un administrateur local la gestion des accès de son bâtiment»
- **FR-07 · Minor · home audience card** — «… la remise au client et le support ensuite.» → «… la remise au client et le suivi après la remise.»
- **FR-08 · Minor · integrators** — «gèrent leurs propres personnes, clés et cartes» → «gèrent eux-mêmes leurs utilisateurs, leurs clés et leurs cartes»
- **FR-09 · Minor · setup lead** — «une recommandation de lecteur avec sa raison» → «… et sa justification»
- **FR-10 · Minor · contact lead** — «Vous préparez l’accès d’un bâtiment» → «Vous planifiez le contrôle d’accès d’un bâtiment»
- **FR-11 · Minor · /about H1** — «L’équipe derrière SmartphoneKey» → «L’équipe SmartphoneKey»
- **FR-12 · Minor · integrators next step** — «Parlons de notre collaboration» → «Parlons d’une collaboration»
- **FR-13 · Minor · setup installer rule** — «… et qui assure ensuite le support du site.» → «… et décidez qui assurera ensuite le suivi du site.»
- **FR-14 · Minor · contact validation** — «Utilisez 160 caractères au maximum pour l’entreprise.» (also the 100 and 4,000 variants) → «Le nom de l’entreprise ne doit pas dépasser 160 caractères.»
- **FR-15 · Minor · preview banner** — «Ce n’est pas le site officiel» → «Ce n’est pas le site public»
- **FR-16 · Minor · /resources lead** — «questions de préparation» → «questions de planification»
- **FR-17 · Minor · LTE guide** — «le lecteur rejoint le propre réseau du site» → «le lecteur se connecte au réseau du site»
- **FR-18 · Minor · /compatibility, Scenario Builder row** — «Chaque scénario actuel appartient …» → «Pour l’instant, chaque scénario appartient …»

### 2. Terminology consistency
The terms are consistent: site, lecteur, contrôleur d’accès, clé Wallet, clé numérique, carte NFC, révoquer, en attente / confirmée / en échec, administrateur de site, titulaire de clé, prestataire, Instructions vs Guides. Product names are correct in `fr.po`.
- **FR-19 · Should fix · header action, mobile menu, footer, CTAs, breadcrumb, property-managers, contact** — «Recommandations de site» sits next to the H1 «Recommandations pour votre site». On its own, "site" reads as "website". Running text inherits it: «… pour les recommandations de site», «Vos réponses aux recommandations de site». → «Recommandations pour votre site» as the one label. It is 256 px in the Spanish header at 1024, so the French equivalent fits.
- **FR-20 · Minor · several pages** — "support" is used three ways: «contactez le support», «Rétablissement et support», «assurer le support». → «assistance» for customer support, «suivi» for the installer's role.
- **FR-21 · Minor · navigation, /resources** — «Archive des articles» → «Archives des articles»

### 3. Semantic fidelity
`fr.po` is faithful. The visible C05 and lead problems are X1:
- /compatibility: «… avec un appareil de programmation SmartphoneKey compatible, y compris le programmateur intégré du lecteur lorsqu'il est disponible.» and «Le processus documenté mentionne DESFire EV3.»
- MIFARE guide lead: «Un programmateur compatible ou le programmateur intégré …»
- Guide titles: «Programmation MIFARE Classic et DESFire EV3»
- The old offline lead
- The H1 «Matter et Thread pour le contrôle d'accès.»

### 4. Interface strings
- **FR-22 · Should fix · /about** — «Advisor» appears three times; the `fr.po` msgstr is literally "Advisor". → «Conseiller» / «Conseillère» per person, or «Membre du comité consultatif».
- **FR-23 · Should fix · /contact form label** — «Sur quoi pouvons-nous vous aider ? (obligatoire)» → «En quoi pouvons-nous vous aider ? (obligatoire)»
- **FR-24 · Minor · contact prefill note** — «Vos réponses aux recommandations de site sont déjà reportées ci-dessous.» → «Les réponses saisies dans « Recommandations pour votre site » sont reportées ci-dessous. Modifiez-les si nécessaire.»
- **FR-25 · Minor · setup result label** — «Guides pour votre sélection» → «Guides liés à vos réponses»
- Checked and correct: the status, error, conflict and preview messages, «Votre demande a bien été reçue.», the field errors after an empty submit, captions, the language names, and 404.

### 5. Layout (fr)
H1 line counts are 3 or fewer at both widths. The 3-line H1s at 390 are home, readers, property-managers, integrators (3/3), MIFARE (3/3) and offline.
- **FR-26 · Should fix · MIFARE guide H2** — «Pourquoi les autres générations et tailles nécessitent une confirmation» takes 4 lines at 390. → «Pourquoi confirmer les autres générations et tailles»

### 6. Metadata (fr)
- **FR-27 · Minor · /find-your-setup title** — «Contrôle d’accès : recommandations pour votre site | SmartphoneKey» is 66 characters. → «Recommandations pour votre site | SmartphoneKey» (47)
- Home (65), compatibility (65) and the offline guide (65) are at the limit.
- The descriptions over 160 (MIFARE guide 183, offline guide 162) are X1; the catalogue values are 152 and 153.

(FR Should fix: FR-01, 02, 03, 19, 22, 23, 26. Minor: the remaining 20.)

---

## German (de)

- "Sie" is used consistently, with no "du" forms.
- No forbidden content appears in `de.po`. The failover negation is kept: «Das bedeutet keinen automatischen Failover.»
- The English-only note «Diese Seite ist auf Englisch. Eine geprüfte Übersetzung ist nicht verfügbar.» is present.

### 1. Naturalness and idiom
- **DE-01 · Should fix · /compatibility #cards** — «Ein Familienname deckt nicht jede Speichergröße, jedes Zutrittsdatenformat und nicht jede Karte eines anderen Anbieters ab.» «Familienname» means a person's surname. → «Die Bezeichnung einer Kartenfamilie umfasst nicht jede Speichergröße, jedes Zutrittsdatenformat oder jede Karte eines anderen Anbieters.»
- **DE-02 · Should fix · /products/readers** — «Kompatible Schlosstechnik und alle Geräte zum Verlassen, die die Tür benötigt» is a calque of "exit devices". → «Kompatible Schlosstechnik und, falls nötig, Ausgangstaster oder Fluchttürtechnik»
- **DE-03 · Should fix · nav, footer, breadcrumb, home, property-managers, setup links** — «Immobilienteams» (also «Für Immobilienteams», «So nutzen Immobilienteams SmartphoneKey») is a calque. → «Immobilienverwaltung», «Für die Immobilienverwaltung», «So nutzt die Immobilienverwaltung SmartphoneKey»
- **DE-04 · Minor · home, access-management** — «Aktivitäts- und Prüfprotokolle» («Prüfprotokoll» usually means a test report) → «Aktivitäts- und Audit-Protokolle»
- **DE-05 · Minor · home strip and H2, /platform diagram** — «So gelangen Personen hinein» → «Zugang an der Tür»
- **DE-06 · Minor · readers and LTE guide table** — the row header «Damit es funktioniert» is vague. → «Für den laufenden Betrieb»
- **DE-07 · Minor · readers FAQ** — «keine einzelne Entfernung passt zu jeder Anlage» → «einen Abstand, der für jede Anlage gilt, gibt es nicht»
- **DE-08 · Minor · /platform steps** — «… oder die Person geht» → «… oder die Person auszieht oder ausscheidet»
- **DE-09 · Minor · property-managers** — «Zutritt für den Auftrag, wo unterstützt befristet, und entziehen Sie ihn» → «Zutritt für den Auftrag – wo unterstützt, auch befristet – und entziehen Sie ihn, wenn die Arbeit endet.»
- **DE-10 · Minor · access-management example steps** — «Wählen / den Standort und die Türen» → «Auswählen / Standort und Türen»; «Prüfen / ob die Leser bestätigt haben»
- **DE-11 · Minor · home, existing users** — «oder laden Sie die App» → «… oder laden Sie die App herunter»
- **DE-12 · Minor · /about** — «Beirat» names the board, not a person. → «Beiratsmitglied»

### 2. Terminology consistency
The terms are consistent: Standort, Leser, Zutrittscontroller, Wallet-Schlüssel, digitaler Schlüssel, NFC-Karte, entziehen, ausstehend / bestätigt / fehlgeschlagen, Standortadministrator, Dienstleister, Anleitungen vs Ratgeber, «Standortempfehlungen» with the H1 «Empfehlungen für Ihren Standort». The visible «Workflow», «Programmiergerät», «Vorgang», «Benutzerhandbuch», «Verriegelungstechnik» and «Leserrevision» are X1.
- **DE-13 · Minor · /platform and /solutions/integrators meta descriptions** — «Leser mit Controller» drops "built-in". → «Leser mit integriertem Zutrittscontroller»
- **DE-14 · Minor · several pages** — «Installation» and «Anlage» are mixed for the installed system. → «Anlage» for the system, «Installation» for the act of installing.
- **DE-15 · Minor · access-management button** — «Anleitung zum Admin Panel lesen», while the footer says «Anleitung für das Admin Panel». → «Anleitung für das Admin Panel lesen»
- **DE-16 · Minor · /about, team title** — the job title «Chief Artificial Intelligence Officer» is left in English in `de.po`. It also makes the team page title 69 characters. → «Leiter Künstliche Intelligenz»

### 3. Semantic fidelity
The C05 problems are X1: «… mit einem kompatiblen SmartphoneKey-Programmiergerät, einschließlich des im Leser integrierten Programmiergeräts …», «Der dokumentierte Workflow nennt DESFire EV3.», the MIFARE lead with «Programmiergerät», and the old offline, LTE and Matter leads.
- **DE-17 · Should fix · /compatibility meta description** — «welche Matter-Funktionen gelten» changes "are supported" to "apply" and loses the limitation. → «welche Matter-Funktionen unterstützt werden»
- **DE-18 · Minor · /compatibility FAQ, MIFARE guide** — «Kann ich Karten mit der Lösung eines Drittanbieters programmieren?» / «… keine Kartenprogrammierung durch Drittanbieter.» This reads like a service, and could be taken to rule out pre-encoded cards. → «Kann ich ein Kartenprogrammiergerät eines Drittanbieters verwenden?» / «Programmiergeräte von Drittanbietern unterstützt SmartphoneKey nicht.»
- **DE-19 · Minor · property-managers meta description** — «Mitarbeitende und Dienstleister verwalten … Probleme erkennen» → «Zutritt für Mitarbeitende und Dienstleister verwalten … Probleme gebäudeübergreifend erkennen»
- **DE-20 · Minor · MIFARE guide description** (`de.po`) — «Was vor der Bestellung zu prüfen ist.» drops "how it works". → «So funktioniert es und das sollten Sie vor der Bestellung prüfen.»
- **DE-21 · Minor · integrators, Assess step** — «und alle vernetzten Geräte» → «und etwaige vernetzte Geräte»
- **DE-22 · Minor · offline guide H2** (`de.po`) — «Wiederverbindung und Support» → «Wiederherstellung und Support»

### 4. Interface strings
- **DE-23 · Should fix · guides, /compatibility, archive** — «Produktangaben geprüft 27 Oktober 2026», «Veröffentlicht 12 November 2025». This is X2. → «27. Oktober 2026»
- **DE-24 · Minor · preview banner** — «Dies ist nicht die Live-Seite» → «Dies ist nicht die öffentliche Website»
- **DE-25 · Minor · contact validation** — «Geben Sie Ihren Namen ein, zwischen 2 und 120 Zeichen.» → «Geben Sie Ihren Namen ein (2 bis 120 Zeichen).»
- **DE-26 · Minor · setup result label** — «Warum» → «Begründung»
- **DE-27 · Minor · contact aside H2** — «Suchen Sie zuerst Antworten?» → «Lieber erst selbst nachlesen?»
- Checked and correct: navigation, form labels, «Bitte wählen», the status messages «Wird gesendet…» and «Bitte prüfen Sie die markierten Felder.», «Ihre Anfrage ist eingegangen.», the result labels «Ihre Auswahl / Empfehlung / Vor Ort noch zu prüfen / Ratgeber zu Ihrer Auswahl», 404, and the language names.

### 5. Layout (de)
- H1 line counts are 3 or fewer at both widths: property-managers is 3/3, and the 3-line H1s at 390 are home, readers, integrators and MIFARE. No H2 reaches 4 lines.
- The longest heading compound, «Zutrittscontroller» (18 characters), does not overflow at 390.
- The header action «Standortempfehlungen» (202 px) fits at 1024.

### 6. Metadata (de)
All titles are 65 characters or fewer; the MIFARE guide at 65 is X1, with 61 in the catalogue. The description over 160 (MIFARE guide 181) is X1; the catalogue value is 153.

(DE Should fix: DE-01, 02, 03, 17, 23. Minor: the remaining 22.)

---

## Spanish (es)

- "usted" is used throughout, with no "tú".
- No forbidden content appears, and the English-only note is present.
- The third-party FAQ is correct: «SmartphoneKey no admite equipos de terceros para programar tarjetas».

### 1. Naturalness and idiom
- **ES-01 · Should fix · CTAs on home, platform, access-management, property-managers, setup, visitor, security, resources, guides, contact title** — «Hable de su proyecto», «Hable de sus inmuebles», «Hable de estas recomendaciones», «Hable de los visitantes» (which reads as "talk about the visitors"), «Hable de requisitos técnicos». → «Háblenos de su proyecto», «Háblenos de sus inmuebles», «Comente estas recomendaciones con nosotros», «Consúltenos sobre el acceso de visitantes», «Consúltenos sus requisitos técnicos»
- **ES-02 · Should fix · property-managers lead** — «Dé acceso cuando un residente se instala y revóquelo cuando se marcha. Dé al personal las puertas que necesita su trabajo, dé a los contratistas acceso para el trabajo …» → «Dé acceso a cada residente al instalarse y revóquelo cuando se marche. Dé al personal acceso a las puertas que necesita y a los contratistas acceso para cada trabajo, y vea qué edificios requieren atención.»
- **ES-03 · Should fix · /platform steps, property checklist, setup rule** — «Emita el acceso», «Quién emite y revoca el acceso» → «Conceda el acceso», «Quién concede y revoca el acceso»
- **ES-04 · Should fix · home task** — «Termine el acceso cuando acabe el trabajo …» → «Ponga fin al acceso al terminar el trabajo y compruebe que cada lector ha aplicado el cambio.»
- **ES-05 · Should fix · visitor H1** (extra page) — «Facilite que los visitantes lleguen a la persona adecuada» → «Ayude a los visitantes a contactar con la persona adecuada»
- **ES-06 · Should fix · MIFARE guide body** — «La Guía de usuario del Admin Panel se describe cada pantalla.» is ungrammatical; `es.po` msgid "describes each screen." has msgstr «se describe cada pantalla.». → msgstr «describe cada pantalla.»
- **ES-07 · Minor · home, property-managers** — «Deje que un administrador local gestione …» → «Permita que un administrador local gestione el acceso de su edificio.»
- **ES-08 · Minor · integrators** — «gestionan a sus propias personas, llaves y tarjetas» → «gestionan las personas, llaves y tarjetas de sus propios sitios»
- **ES-09 · Minor · contact prefill, property checklist intro** — «Sus respuestas de Recomendaciones para su sitio ya están rellenadas más abajo.» → «Hemos rellenado el formulario con sus respuestas de «Recomendaciones para su sitio». Puede cambiarlas.»
- **ES-10 · Minor · readers FAQ** — «ninguna distancia única sirve para todas las instalaciones» → «no hay una distancia que sirva para todas las instalaciones»
- **ES-11 · Minor · /about** — «El equipo detrás de SmartphoneKey» / «Vea lo que construimos» → «El equipo de SmartphoneKey» / «Descubra lo que hacemos»
- **ES-12 · Minor · /platform illustration** — «Bicicletero» means a bike rack. → «Cuarto de bicicletas»
- **ES-13 · Minor · 404** — «Esta página no está aquí.» → «No encontramos esta página.»
- **ES-14 · Minor · integrators** — «Trate con nuestro equipo la distribución …» → «Hable con nuestro equipo sobre distribución, integración, servicio y marca.»

### 2. Terminology consistency
The terms are consistent: sitio, lector, controlador de acceso, llave en Wallet, llave digital, tarjeta NFC, revocar, pendiente / confirmado / fallido, administrador del sitio, titular de llaves, Instrucciones vs Guías, «Recomendaciones para su sitio» on every link and as the H1. The visible «instalación» for site in the old guide texts is X1.
- **ES-15 · Should fix · home tool, setup, contact, readers table, LTE guide** — «Celular (LTE)» and «cobertura celular» are Latin American, while the rest of the copy is peninsular («vídeo», «móvil»). → «Red móvil (LTE)», «cobertura móvil», «servicio móvil»
- **ES-16 · Should fix · nav, mobile menu, footer, breadcrumb** — «Gestión de inmuebles» names an activity, next to «Instaladores e integradores», which names people. The body uses «equipos de gestión de inmuebles». → «Gestores de inmuebles» everywhere
- **ES-17 · Minor · preview banner** — «No es el sitio real», where "sitio" also means a building on this site. → «No es el sitio web real»
- **ES-18 · Minor · /compatibility next step** — «No envíe llaves, contraseñas ni secretos de tarjeta.» → «No envíe claves, contraseñas ni secretos de tarjeta.»
- **ES-19 · Minor · footer, CTAs** — «Conviértase en socio», where «socio» can read as shareholder. → «Colabore con nosotros»
- **ES-20 · Minor · /about** — «Consejo asesor» names the board. → «Miembro del consejo asesor»
- **ES-21 · Minor · privacy, terms** — the closing line «Questions about this page: info@smartphonekey.com.» is in English on every language. The catalogue entry is empty because the view is English-only. → Translate this one line, or move it outside the English-only body.

### 3. Semantic fidelity
The C05 problems are X1: «… con un dispositivo de programación SmartphoneKey compatible, incluido el programador integrado …», «Programación de credenciales mediante el flujo de trabajo …», «Un programador compatible o el programador integrado admitido del lector escribe la credencial …», and the old offline, LTE and Matter leads.
- **ES-22 · Minor · home, setup, automation** — «Cada escenario se ejecuta en un solo hub y en los dispositivos puestos en servicio en él» says the scenario runs on the devices. → «… en un solo hub, con los dispositivos puestos en servicio en él»

### 4. Interface strings
- **ES-23 · Should fix · guides, /compatibility, archive** — «Publicado 12 noviembre 2025», «Datos del producto comprobados 27 octubre 2026». This is X2. → «12 de noviembre de 2025»
- **ES-24 · Should fix · setup, home tool, contact, CTAs** — buttons are in the infinitive («Ver recomendaciones», «Empezar de nuevo», «Enviar consulta»), while links next to them are in the imperative («Cambie las respuestas», «Compruebe la compatibilidad», «Explore la plataforma», «Lea las guías»). → infinitive for every button and action link («Cambiar respuestas», «Comprobar compatibilidad», «Explorar la plataforma», «Leer las guías»)
- **ES-25 · Minor · contact validation** — «Introduzca su nombre, de entre 2 y 120 caracteres.» → «Introduzca su nombre (entre 2 y 120 caracteres).»
- **ES-26 · Minor · archived-article note** — «consulte Cómo funciona SmartphoneKey y Compruebe la compatibilidad.» → «consulte «Cómo funciona SmartphoneKey» y la página de compatibilidad.» (needs its own msgid)
- **ES-27 · Minor · comparison table header** — «En qué se diferencian» repeats the caption. → «Aspecto»
- Checked and correct: language names, the mobile menu, breadcrumbs, the result labels «Su selección / Recomendación / Por qué / Por comprobar in situ / Guías para su selección», status and validation messages, and «Hemos recibido su consulta.»

### 5. Layout (es)
- H1 line counts are 3 or fewer: integrators is 3/3, and compatibility, readers, MIFARE, offline and home are 3 at 390. No H2 reaches 4 lines.
- The widest header action is «Recomendaciones para su sitio» (256 px at 1280, 248 px at 1024), on one line.
- «Ver recomendaciones completas» (264 px) fits on one line at 390.

### 6. Metadata (es)
- At 65 characters: platform and setup. At 160: property-managers.
- The MIFARE guide description (184) and the offline guide title (69) are X1; the catalogue values are 155 and 61.
- Titles that read as a command rather than a search result: «Hable de su proyecto de control de accesos | SmartphoneKey» (see ES-01) → «Su proyecto de control de accesos | SmartphoneKey».

(ES Should fix: ES-01 to 06, 15, 16, 23, 24. Minor: the remaining 17.)

---

## Layout summary: H1 and largest H2 line counts (1280/390)

| Page | EN | UK | FR | DE | ES |
|---|---|---|---|---|---|
| home | 2/3 · 2/2 | 2/3 · 2/3 | 2/3 · 2/3 | 2/3 · 2/3 | 2/3 · 2/3 |
| platform | 1/2 · 2/2 | 1/2 · 2/2 | 2/2 · 2/3 | 2/2 · 2/3 | 2/2 · 2/2 |
| access-management | 2/2 · 1/2 | 2/2 · 2/2 | 2/2 · 2/2 | 2/2 · 2/2 | 2/2 · 1/2 |
| readers | 2/2 · 3/3 | 2/3 · 3/3 | 2/3 · 3/3 | 2/3 · 3/3 | 2/3 · 3/3 |
| compatibility | 2/2 · 1/1 | 2/2 · 1/2 | 2/2 · 1/2 | 2/2 · 1/1 | 2/3 · 1/2 |
| property-managers | 2/2 · 2/2 | 2/3 · 2/2 | 2/3 · 2/2 | 3/3 · 2/3 | 2/2 · 1/2 |
| integrators | 2/2 · 2/2 | **3/4** · 2/2 | 3/3 · 2/2 | 2/3 · 2/3 | 3/3 · 2/2 |
| setup (with result) | 2/2 · 1/1 | 2/2 · 1/1 | 2/2 · 1/1 | 2/2 · 1/1 | 1/2 · 1/1 |
| contact | 1/2 · 1/1 | 2/2 · 1/1 | 2/2 · 1/1 | 2/2 · 1/1 | 2/2 · 1/1 |
| resources | 1/1 · 1/2 | 1/1 · 1/2 | 1/1 · 1/2 | 1/2 · 1/2 | 1/1 · 1/2 |
| MIFARE guide | 2/3 · 2/2 | 3/3 · **2/4** | 3/3 · **2/4** | 3/3 · 2/3 | 2/3 · 2/3 |
| offline guide | 2/2 · 1/2 | 3/3 · 1/2 (stale H1) | 2/3 · 1/2 | 2/2 · 1/2 | 2/3 · 1/2 |

Across all four languages and both widths:
- no element overflows or is clipped;
- no page scrolls horizontally;
- no table cell overflows;
- every button sits on one line at 390;
- the header action fits at 1280 and 1024;
- the mobile menu is complete and scrolls.

---

## The fifteen most important fixes

1. **all four · /compatibility, the four guides, /resources, team meta** · stale record translations, e.g. uk «… за допомогою сумісного пристрою для програмування SmartphoneKey, зокрема вбудованого програматора зчитувача …» → «Програмується з Admin Panel на зчитувачі SmartphoneKey із підтримкою програмування.» Fix: reload with `--i18n-overwrite`, force-update the `noupdate` records, restart, then re-check (X1).
2. **es · MIFARE guide** · «La Guía de usuario del Admin Panel se describe cada pantalla.» → «La Guía de usuario del Admin Panel describe cada pantalla.»
3. **fr · /compatibility** · «Un nom de famille ne couvre ni …» → «Le nom d’une famille de cartes ne couvre ni …»
4. **de · /compatibility** · «Ein Familienname deckt nicht …» → «Die Bezeichnung einer Kartenfamilie umfasst nicht …»
5. **uk · /solutions/integrators** · «Встановлюйте, передавайте й підтримуйте системи доступу» (4 lines at 390) → «Монтаж, передача й підтримка систем доступу»
6. **de, es · guides, /compatibility, archive** · «27 Oktober 2026» / «27 octubre 2026» → «27. Oktober 2026» / «27 de octubre de 2026» (use the locale's long format in `rendering.py`)
7. **fr · header, footer, CTAs** · «Recommandations de site» → «Recommandations pour votre site»
8. **fr · /about** · «Advisor» → «Conseiller» / «Conseillère»
9. **de · nav, home, property-managers** · «Immobilienteams» → «Immobilienverwaltung»
10. **es · CTAs and contact title** · «Hable de su proyecto» → «Háblenos de su proyecto»
11. **fr · /contact form** · «Sur quoi pouvons-nous vous aider ?» → «En quoi pouvons-nous vous aider ?»
12. **es · home tool, setup, contact, readers** · «Celular (LTE)» / «cobertura celular» → «Red móvil (LTE)» / «cobertura móvil»
13. **de · /products/readers** · «alle Geräte zum Verlassen, die die Tür benötigt» → «und, falls nötig, Ausgangstaster oder Fluchttürtechnik»
14. **uk · MIFARE guide** · «Зчитування, програмування, надання доступу та використання картки» (4 lines at 390) → «Чотири окремі операції з карткою»
15. **uk · home, access-management** · «Історія дій і записи аудиту» → «Журнал дій і аудиту»
