# Ukrainian editorial review – homepage update of 30 October 2026

**Summary.** The 93 new Ukrainian strings are accurate and publishable: product names are exact, every limitation in the English survives, no forbidden content appears, and the captions say the interface is English wherever the English caption does. Nothing is blocking.
Six strings should be reworded before release: one misreads "still" and departs from the established failover wording, one uses a different "site team" / "entrance" term than the rest of the site, three carry a word-for-word calque ("shown before anything is sent", "It is separate from"), and one key status sentence is ambiguous; twelve smaller points are style or one-term-one-translation consistency.

**Counts.** Reviewed: 93 (uk) · Blocking: 0 · Should-fix: 6 · Minor: 12

Reviewed sources: `translations-2026-10-30.json` (uk), `i18n/uk.po` for existing terms, rendered `/uk`, `/uk/platform`, `/uk/platform/access-management`, `/uk/products/readers`, `/uk/platform/visitor-access` (server HTML via curl). Two of the 93 strings ("Ask us to review the site…", "Issue and revoke Wallet keys…") do not render on these five pages; they were reviewed in the JSON only.

## Checks that passed

- Register: polite "ви", imperatives for tasks ("Додавайте", "Видайте", "Скасуйте", "Перевірте"); owner's direction pairs used where the meaning matches ("Зчитувач і контролер доступу в одному пристрої", "Скасуйте доступ і перевірте, що зчитувачі застосували зміну").
- Terms match the glossary and the existing catalogue: об’єкт, зчитувач, контролер доступу, ключ у Wallet, NFC-картка, цифровий ключ, мешканець, персонал, підрядник, відвідувач, власник ключа, скасувати (revoke), очікує / підтверджена / не вдалася, mesh-мережа Thread, Border Router, хаб.
- Limitations kept: "підтримуваний / де це підтримується" (7 strings), "залежать від … монтажу/об’єкта", "а не наданий доступ", "а не доказ, що людина пройшла", "Доступні дії залежать від ваших прав і налаштувань об’єкта", "Функції контролера Matter підтверджуються для кожного проєкту", "Цифри — значення інтерфейсу тестового облікового запису".
- Names exact: SmartphoneKey, Admin Panel, Apple Wallet, Google Wallet, MIFARE Classic, MIFARE DESFire EV3, Matter, Thread, LTE, Wi-Fi, ChatGPT, AI Concierge, AI Assistant; UI labels Dashboard, Give Access, Assign Key, Guest Key, Wallet Key, Devices left in English in captions.
- Forbidden content: none (no distance, only EV3, no memory sizes, "підтримуваних пристроїв Matter", no "unlimited", AI Concierge only "запитайте про версію та доступність", failover only as the negative statement, no prices, no demo booking, no programmer wording, no "revoke instantly" / "handles the rest").
- Headings: sentence case, no trailing full stop; home H1 (existing string) is 49 characters; longest new H2 "Зчитувач і контролер доступу в одному пристрої" is 46 characters, two lines on a phone.
- Captions: "Інтерфейс англійською" present on every caption whose English says "English interface"; absent where the English omits it (home "Recent activity" caption).

## Findings

### Blocking

None.

### Should-fix

| # | English (shortened) | Current Ukrainian | Proposed Ukrainian | Reason |
|---|---|---|---|---|
| S1 | Mesh coverage and the route to the internet still depend… automatic failover is not implied. | Покриття mesh-мережі та шлях до інтернету, як і раніше, залежать від розташування, живлення та будівлі. Скільки зчитувачів ділять одне підключення і що станеться, якщо воно зникне, залежить від конкретного монтажу; автоматичне перемикання не мається на увазі. Функції контролера Matter підтверджуються для кожного проєкту. | Покриття mesh-мережі та шлях до інтернету все одно залежать від розташування, живлення та будівлі. Скільки зчитувачів ділять одне підключення і що станеться, якщо воно зникне, залежить від конкретного об’єкта та монтажу; це не означає автоматичного перемикання на резерв. Функції контролера Matter підтверджуються для кожного проєкту. | "як і раніше" means "as before", not "still/nevertheless"; the readers FAQ already says "автоматичного перемикання на резерв", so the same page should use one wording. |
| S2 | Visitors scan the entrance QR code to reach a resident or the site team. | Відвідувачі сканують QR-код на вході, щоб зв’язатися з мешканцем або командою об’єкта. | Відвідувачі сканують QR-код біля входу, щоб зв’язатися з мешканцем або персоналом об’єкта. | /platform, the visitor-access page and its metadata say "QR-код біля входу" and "персоналом об’єкта"; one term, one translation. |
| S3 | Guest Key form in Wallet Key mode: validity dates and the recipient field, shown before anything is sent. English interface. | Форма Guest Key в режимі Wallet Key: дати дії та поле одержувача, показані до будь-якого надсилання. Інтерфейс англійською. | Форма Guest Key у режимі Wallet Key: дати дії та поле одержувача; знімок зроблено до надсилання. Інтерфейс англійською. | "показані до будь-якого надсилання" is a word-for-word calque; the meaning is that nothing had been sent when the screenshot was taken. |
| S4 | Guest Key form in Wallet Key mode: lock selection, validity dates… The dates are the form's defaults at capture time, not a completed grant. English interface. | Форма Guest Key в режимі Wallet Key: вибір замка, дати дії та поле одержувача, показані до будь-якого надсилання. Дати — стандартні значення форми на момент знімка, а не наданий доступ. Інтерфейс англійською. | Форма Guest Key у режимі Wallet Key: вибір замка, дати дії та поле одержувача; знімок зроблено до надсилання. Дати — типові значення форми на момент знімка, а не наданий доступ. Інтерфейс англійською. | Same calque as S3; "типові значення" is the usual term for defaults. The limitation "а не наданий доступ" is kept. |
| S5 | AI Concierge is the visitor-facing service. It is separate from the AI Assistant inside the Admin Panel and from the SmartphoneKey app in ChatGPT. | AI Concierge — це сервіс для відвідувачів. Він окремий від AI Assistant в Admin Panel і від застосунку SmartphoneKey у ChatGPT. | AI Concierge — це сервіс для відвідувачів, окремий від AI Assistant в Admin Panel і від застосунку SmartphoneKey у ChatGPT. | "Він окремий від" is an English structure; one sentence reads naturally and keeps the distinction. |
| S6 | Sending a change is not the same as a reader applying it. The Admin Panel shows whether each change is pending, confirmed by the reader or failed… | Надіслати зміну — не те саме, що зчитувач її застосував. Admin Panel показує, чи кожна зміна очікує, підтверджена зчитувачем або не вдалася, а також які зчитувачі онлайн, офлайн чи не підключені. Скасування, що очікує на зчитувач без зв’язку, на ньому ще не діє. | Надіслана зміна ще не означає, що зчитувач її застосував. Admin Panel показує стан кожної зміни — очікує, підтверджена зчитувачем чи не вдалася — і які зчитувачі онлайн, офлайн чи не підключені. Скасування, що очікує на зчитувач без зв’язку, на ньому ще не діє. | "чи кожна зміна очікує" can be read as "whether every change is pending"; naming the status removes the ambiguity in the sentence that carries the key limitation. |

### Minor

| # | English (shortened) | Current Ukrainian | Proposed Ukrainian | Reason |
|---|---|---|---|---|
| M1 | Reader and access controller in one device. LTE, Wi-Fi or supported Thread connectivity. | …Підключення LTE, Wi-Fi або підтримуване Thread. | …Підключення LTE, Wi-Fi або Thread, де підтримується. | "підтримуване Thread" hangs without a noun; "де підтримується" keeps the limitation and reads naturally. |
| M2 | Combine readers with a built-in access controller and LTE, Wi-Fi or supported Thread connectivity. | …та підключенням LTE, Wi-Fi або підтримуваним Thread. | …та підключенням LTE, Wi-Fi або Thread, де це підтримується. | Same as M1. |
| M3 | Choose connectivity to suit the building. | Обирайте підключення під будівлю. | Обирайте підключення залежно від будівлі. | "під будівлю" is colloquial for a B2B page. |
| M4 | Installer or integrator? | Ви монтажник або інтегратор? | Ви монтажник чи інтегратор? | An alternative question takes "чи". |
| M5 | Give residents, staff and contractors access… update permissions… | …змінюйте права та переглядайте події пристроїв… | …змінюйте права доступу та переглядайте події пристроїв… | The brief and the neighbouring string ("Змінюйте права доступу, коли…") use "права доступу". |
| M6 | Close-up of the … Dashboard: the Give Access button, summary cards and recent activity | …кнопка Give Access, картки зведення та останні події | …кнопка Give Access, підсумкові картки та останні події | "картки зведення" is an unusual genitive chain. |
| M7 | SmartphoneKey Admin Panel showing access actions, device and key summaries, and recent activity | Admin Panel SmartphoneKey з діями доступу, зведеннями пристроїв і ключів та останніми подіями | Admin Panel SmartphoneKey: дії з доступом, зведення пристроїв і ключів та останні події | "з діями доступу" is not idiomatic; a colon list reads naturally in alt text. |
| M8 | The AI Assistant panel as it opens, English interface, before any message is sent. | Панель AI Assistant одразу після відкриття, інтерфейс англійською, до надсилання будь-якого повідомлення. | Панель AI Assistant одразу після відкриття, ще без повідомлень. Інтерфейс англійською. | "до надсилання будь-якого повідомлення" is a calque; same fix family as S3. |
| M9 | Power, compatible lock hardware and local wiring are still required. Network layout and coverage depend on the installation. | …Схема мережі та покриття залежать від конкретного монтажу. | …Схема мережі та покриття залежать від конкретного об’єкта та монтажу. | "depend on the installation" is rendered "від конкретного об’єкта та монтажу" in the example-layout note on the same page; unify (see also S1). |
| M10 | An installer connects the reader, power and compatible lock hardware, then configures the connection. | …а потім налаштовує з’єднання. | …а потім налаштовує підключення. | "connection" is "підключення" in the other new strings ("Порівняти підключення зчитувачів", "Приклад схеми підключення"). |
| M11 | Devices page in the Admin Panel… Interface evidence of monitoring, not a network layout. English interface. | …Це вигляд інтерфейсу моніторингу, а не схема мережі. Інтерфейс англійською. | …Знімок інтерфейсу моніторингу, а не схема мережі. Інтерфейс англійською. | "вигляд інтерфейсу" is vague; "знімок" says it is a screenshot, as the English intends. |
| M12 | Ask us to review the site… or when a third party manages the network. | …або якщо мережею керує стороння компанія. | …або якщо мережею керує стороння організація. | "third party" is wider than a company; "організація" keeps the condition as broad as the English. |

## Notes for the editor

- "Someone leaves" → "Хтось виїжджає або звільняється" names both cases (resident, staff); it adds no fact and reads well; left as is.
- "Authorised door" → "Дозволені двері" is acceptable in the flow diagram; a longer paraphrase would not fit the label.
- Step labels on the home flow mix a noun ("Монтаж", "Вхід") and an imperative ("Надайте доступ"); only "Enter" → "Вхід" is among the new strings and is fine as a step name.
