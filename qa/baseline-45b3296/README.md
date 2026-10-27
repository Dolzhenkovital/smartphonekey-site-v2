# Baseline capture, revision 45b3296 (27 October 2026)

Environment: local Odoo 18 test instance (Docker `odoo:18.0`, build 18.0-20260409, `spk_website_v2` 18.0.2.1.0 with `spk_website_v2.preview_mode=True`, so the 40 px preview banner is present) and the GitHub Pages review copy https://dolzhenkovital.github.io/smartphonekey-site-v2/ built from the same revision. Headless Chrome via puppeteer-core, `load` event plus 1.2 s, General Sans from Fontshare (Latin pages) and the system sans on Ukrainian pages.

Files: the 57 `*.jpg` files without a prefix are the QA screenshots recorded with revision 45b3296 (`qa/screenshots` at that time). `local-*` and `pages-*` are the new captures of this baseline at 1280×800, 1440×900 and 390×844 (`-full` = full page). The `local-en-*` files show Ukrainian because the local Odoo instance remembered the Ukrainian language cookie between captures; use the `pages-en-*` files for English.

Measurements (`capture-log.txt`), the "button" is the first `.button` inside `main`:

| Page | Viewport | H1 size | H1 lines | First primary action top (px) |
|---|---|---|---|---|
| EN home (pages) | 1280×800 | 92.8 px | 3 | 661 |
| EN home (pages) | 1440×900 | 96 px | 3 | 713 |
| EN home (pages) | 390×844 | 44 px | 2 | 398 |
| UK home | 1280×800 | 92.8 px | 4 | 755 |
| UK home | 1440×900 | 96 px | 3 | 728 |
| UK home | 390×844 | 44 px | 3 | 470 |
| EN readers | 1280×800 | 59.5 px | 2 | 4959 (closing section) |
| UK readers | 1280×800 | 59.5 px | 2 | 5204 (closing section) |
| EN platform | 1280×800 | 59.5 px | 3 | 4758 (closing section) |
| UK platform | 1280×800 | 59.5 px | 4 | 5012 (closing section) |

Observations: the home H1 is 93–96 px and takes three to four lines in Ukrainian; the primary action sits at the bottom edge of a 1280×800 viewport (755 px with the banner); the readers and platform pages have no action in their opening, the first button is the closing section 5 000 px down; page heights are 4 600–8 000 px of mostly text.
