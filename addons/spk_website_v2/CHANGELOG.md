# Changelog

## [4.0.0] - 2026-10-30

Module version 18.0.4.0.0. The home page is recomposed around real Admin Panel screenshots captured on 30 October 2026, and the platform, access-management and readers pages gain targeted changes.

- The home page opens with the Admin Panel Dashboard beside the reader, then three benefits, the path from installation to entry (with the Assign Key wizard), everyday situations (with the Guest Key form and recent activity), the built-in AI Assistant, the reader with an example connection layout, additional capabilities and the closing actions. The compact recommendations tool left the home page; `/find-your-setup` still accepts its `site` parameter.
- The platform page opens with the Dashboard close-up and shows the Devices-page filters; the access-management page shows the Assign Key wizard, the Guest Key form, recent activity and the AI Assistant; the readers page explains the shared connection with an example layout. The visitor-access page states that AI Concierge is separate from the Admin Panel AI Assistant and the ChatGPT app.
- Screenshots open in an expanded view (`expand.js`): a modal dialog with a close button, Escape and focus return; without JavaScript the link opens the image.
- New claim C21 (Admin Panel AI Assistant, UI-observed on 30 October 2026, stored as code-supported) in the claim register; new records in a `noupdate` file are created on upgrade, existing records are left alone.
- Four translation catalogues extended with the 93 new strings; the English interface of the screenshots is kept in every language.

## [3.0.0] - 2026-10-27

Module version 18.0.3.0.0. The site has a new visual design: the Manrope typeface (self-hosted, one face for every language), a cool light page with a single teal for actions, links and evidence, a header with a row for existing users (Instructions, Admin Panel) and the language menu above the main navigation, a mobile menu that groups the same destinations, a quieter footer, and the shared page patterns the revised pages are built from (product panel, system strip, task sequence, comparison row, audience paths, capabilities list, workflow illustration, recommendation result). Page content follows in the same release.

- The home, readers, compatibility and platform pages carry the revised English copy: everyday access tasks first, ways to enter, events and status, readers with a built-in access controller, additional capabilities, and the recommendations tool near the end. Card programming is described as a reader capability and no longer as a lead message; the LTE and Wi-Fi comparison lists only what differs.
- Upgrading overwrites editor changes to the claim register, the compatibility rows and the four guides: this release reloads those records so that existing databases receive the clarified card-programming wording, and republishes the MIFARE Classic and MIFARE DESFire EV3 rows. Re-apply any editor changes to those records after the upgrade.

## [2.1.0] - 2026-10-27

- The website is available in French, German, Spanish and Ukrainian as well as English, with a language menu on every page.
- Every page links to the installation and connection instructions from the header, and certifications have their own place in the menu.
- The reader pages explain that every reader can act as a Thread Border Router and as part of the Thread mesh, without separate firmware.

## [2.0.0] - 2026-10-27

- The SmartphoneKey website presents the access control management platform: a new home page with a setup tool, platform, solution, reader, compatibility, security and resource pages.
- Visitors can get a setup starting point without sharing contact details, and can discuss a project, compatibility, integration, partnership or a walkthrough through one enquiry form.
- Four buyer guides: LTE or Wi-Fi, card programming, Matter and Thread, and what happens when a reader is offline.
- Website enquiries become CRM leads with their context, once each, even when the form is sent twice.
- Content editors maintain guides, compatibility rows, the claim register and team pages; publishers decide what goes live.
- The old Webflow addresses keep working: kept pages move to the new design and the others redirect to their new equivalent.
