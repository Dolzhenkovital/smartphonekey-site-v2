# -*- coding: utf-8 -*-
"""SmartphoneKey website 2.0: the shared site data.

One source for the controllers, the templates, the sitemap, the structured
data and the setup guide's script: routes and their metadata, navigation,
the calls to action, the enquiry form's allowlisted values, the setup-guide
rules and the decision for every URL of the Webflow site.

Copy that belongs to one page stays in that page's template; the facts behind
the technical copy are in the claim register (``spk.website.claim``) and the
compatibility rows (``spk.website.compatibility``).
"""

ORIGIN = "https://smartphonekey.com"
ORGANIZATION_ID = ORIGIN + "/#organization"
WEBSITE_ID = ORIGIN + "/#website"
CONTACT_EMAIL = "info@smartphonekey.com"
# Confirmed official profiles: the ones the current site links from its own footer.
SAME_AS = (
    "https://www.linkedin.com/company/smartphonekey/",
    "https://www.facebook.com/smartphonekey/",
    "https://www.instagram.com/smartphonekey_/",
)
OG_IMAGE = {"path": "/spk_website_v2/static/src/img/og-default.png", "width": 1200, "height": 630,
            "alt": "SmartphoneKey reader beside the SmartphoneKey key logo"}
LOGO_PATH = "/spk_website_v2/static/src/img/brand-mark.png"

# The date the 2.0 copy was settled; product evidence was checked a day earlier.
EDITORIAL_DATE = "2026-10-27"
EVIDENCE_DATE = "2026-10-26"

# --- Routes -------------------------------------------------------------------
# path -> template, metadata and breadcrumb trail. ``kind`` picks the
# structured data (see controllers/seo.py); ``index`` False adds noindex.
ROUTES = {
    "/": {
        "template": "spk_website_v2.page_home",
        "title": "Access Control Management Platform | SmartphoneKey",
        "description": "Manage sites, people, keys and connected devices with SmartphoneKey. "
                       "Explore the platform, compare LTE and Wi-Fi readers, and find a setup for your property.",
        "label": "Home",
        "kind": "home",
        "crumbs": (),
    },
    "/platform": {
        "template": "spk_website_v2.page_platform",
        "title": "Access Control Platform for Sites and People | SmartphoneKey",
        "description": "Explore how SmartphoneKey connects sites, people, credentials, readers and supported "
                       "devices in one access management workflow.",
        "label": "Platform",
        "kind": "webpage",
        "crumbs": (),
    },
    "/platform/access-management": {
        "template": "spk_website_v2.page_access_management",
        "title": "Multi-Site Access Management and Credentials | SmartphoneKey",
        "description": "Organise sites, delegate responsibilities and manage supported credentials with clear "
                       "activity and pending-operation states.",
        "label": "Access management",
        "kind": "webpage",
        "crumbs": ("/platform",),
    },
    "/platform/automation": {
        "template": "spk_website_v2.page_automation",
        "title": "Matter Device Automation for Access Environments | SmartphoneKey",
        "description": "Explore practical triggers, conditions and actions for supported Matter devices, with "
                       "clear capability and configuration limits.",
        "label": "Automation",
        "kind": "webpage",
        "crumbs": ("/platform",),
    },
    "/platform/visitor-access": {
        "template": "spk_website_v2.page_visitor_access",
        "title": "QR Intercom and Visitor Access | SmartphoneKey",
        "description": "Understand QR visitor contact and ask about AI Concierge availability and configuration "
                       "for your site.",
        "label": "Visitor access",
        "kind": "webpage",
        "crumbs": ("/platform",),
    },
    "/solutions/property-managers": {
        "template": "spk_website_v2.page_property_managers",
        "title": "Access Control for Property Management | SmartphoneKey",
        "description": "Organise access for residents, staff and contractors across the properties you manage. "
                       "Explore site and credential workflows.",
        "label": "Property managers",
        "kind": "webpage",
        "crumbs": (),
    },
    "/solutions/integrators": {
        "template": "spk_website_v2.page_integrators",
        "title": "Access Control for Installers and Integrators | SmartphoneKey",
        "description": "Evaluate, install, hand over and support customer access systems with SmartphoneKey. "
                       "Explore reader options and partner workflows.",
        "label": "Integrators",
        "kind": "webpage",
        "crumbs": (),
    },
    "/products/readers": {
        "template": "spk_website_v2.page_readers",
        "title": "LTE and Wi-Fi Access Control Readers | SmartphoneKey",
        "description": "Compare SmartphoneKey LTE and Wi-Fi reader configurations, integrated control, supported "
                       "card programming and installation requirements.",
        "label": "Readers",
        "kind": "webpage",
        "crumbs": (),
        "image": {"path": "/spk_website_v2/static/src/img/reader-800.webp", "width": 800, "height": 751,
                  "alt": "SmartphoneKey reader from the current product image library"},
    },
    "/compatibility": {
        "template": "spk_website_v2.page_compatibility",
        "title": "Card and Matter Device Compatibility | SmartphoneKey",
        "description": "Check documented MIFARE Classic and DESFire EV3 programming, Matter capabilities and the "
                       "configuration details needed for your site.",
        "label": "Compatibility",
        "kind": "webpage",
        "crumbs": (),
    },
    "/security": {
        "template": "spk_website_v2.page_security",
        "title": "Access Control Security and Trust | SmartphoneKey",
        "description": "Review scoped permissions, operation visibility, installation boundaries and relevant "
                       "product documentation for your access system.",
        "label": "Security and trust",
        "kind": "webpage",
        "crumbs": (),
    },
    "/resources": {
        "template": "spk_website_v2.page_resources",
        "title": "Access Control Guides and Resources | SmartphoneKey",
        "description": "Find operating instructions and practical guides to credentials, LTE and Wi-Fi, Matter "
                       "and Thread, and offline access management.",
        "label": "Resources",
        "kind": "collection",
        "crumbs": (),
    },
    "/find-your-setup": {
        "template": "spk_website_v2.page_setup",
        "title": "Find an Access Control Setup for Your Site | SmartphoneKey",
        "description": "Explore an access-control planning checklist for your sites, doors and connection options. "
                       "View results without submitting contact details.",
        "label": "Find your setup",
        "kind": "webpage",
        "crumbs": (),
    },
    "/contact": {
        "template": "spk_website_v2.page_contact",
        "title": "Discuss Your Access Control Project | SmartphoneKey",
        "description": "Contact SmartphoneKey about project planning, compatibility, integration, partnership or "
                       "a product walkthrough.",
        "label": "Contact",
        "kind": "contact",
        "crumbs": (),
    },
    "/about": {
        "template": "spk_website_v2.page_about",
        "title": "About SmartphoneKey | Access Control Management",
        "description": "Meet the product and team behind SmartphoneKey and explore our approach to managing access.",
        "label": "About",
        "kind": "about",
        "crumbs": (),
    },
    "/thank-you": {
        "template": "spk_website_v2.page_thank_you",
        "title": "Enquiry Received | SmartphoneKey",
        "description": "Your enquiry has been received.",
        "label": "Enquiry",
        "kind": "webpage",
        "index": False,
        "crumbs": (),
    },
    # Retained URLs of the Webflow site, now in the 2.0 shell.
    "/certifications": {
        "template": "spk_website_v2.page_certifications",
        "title": "Product Certifications and Documents | SmartphoneKey",
        "description": "Open the regulatory records and platform documents published for SmartphoneKey readers "
                       "and check the exact model each one covers.",
        "label": "Certifications",
        "kind": "webpage",
        "crumbs": ("/products/readers",),
    },
    "/apps-and-chatbot": {
        "template": "spk_website_v2.page_apps",
        "title": "SmartphoneKey Mobile Apps and ChatGPT App | SmartphoneKey",
        "description": "Get the SmartphoneKey apps for Android and iPhone, and open the SmartphoneKey app in ChatGPT.",
        "label": "Apps",
        "kind": "webpage",
        "crumbs": ("/resources",),
    },
    "/privacy-policy": {
        "template": "spk_website_v2.page_privacy_policy",
        "title": "Privacy Policy | SmartphoneKey",
        "description": "How SmartphoneKey collects, uses and protects personal information on its website and services.",
        "label": "Privacy Policy",
        "kind": "webpage",
        "crumbs": (),
        # Legal text is carried over unchanged until a reviewed version replaces it.
        "lastmod": None,
    },
    "/terms-of-service": {
        "template": "spk_website_v2.page_terms_of_service",
        "title": "Terms of Service | SmartphoneKey",
        "description": "The terms that apply to the SmartphoneKey website and services.",
        "label": "Terms of Service",
        "kind": "webpage",
        "crumbs": (),
        "lastmod": None,
    },
}
# The new routes of the 2.0 site (the retained Webflow URLs are served through
# the baseline's own route list, see controllers/main.py).
NEW_PATHS = (
    "/", "/platform", "/platform/access-management", "/platform/automation", "/platform/visitor-access",
    "/solutions/property-managers", "/solutions/integrators", "/products/readers", "/compatibility",
    "/security", "/resources", "/find-your-setup", "/contact", "/about", "/thank-you",
)
RESOURCE_PREFIX = "/resources/"
POST_PREFIX = "/post/"
TEAM_PREFIX = "/team/"

# Served by the ``smartphonekey`` module (the instruction site). They stay
# where they are, in their own languages; the marketing site links to them
# (Odoo adds the visitor's language prefix, which the instruction site honours).
# The existing installation and connection guide (served by ``smartphonekey``,
# in every site language): the site's "Instructions" link, as on the old site.
INSTALLATION_GUIDE = "/guide-for-usage-and-installation"
INSTRUCTION_PATHS = {
    "/guide-for-usage-and-installation": "Installation and connection guide",
    "/instructions/admin-guide": "Admin Panel user guide",
    "/instructions/admin-panel": "Admin Panel walkthrough",
    "/instructions/mobile-app-guide": "Mobile app user guide",
    "/instructions/mobile-app": "Mobile app walkthrough",
}

# --- Languages ------------------------------------------------------------
# (url code, Odoo language code, native name). English is the default and
# lives at the root; the others under /fr/, /de/, /es/, /uk/ (Odoo's own
# website language prefixes). Never chosen by IP address.
SITE_LANGS = (
    ("en", "en_US", "English"),
    ("fr", "fr_FR", "Français"),
    ("de", "de_DE", "Deutsch"),
    ("es", "es_ES", "Español"),
    ("uk", "uk_UA", "Українська"),
)
DEFAULT_LANG = "en"
OG_LOCALES = {"en": "en_GB", "fr": "fr_FR", "de": "de_DE", "es": "es_ES", "uk": "uk_UA"}
# Pages kept in English in every language: legal text needs a reviewed
# translation, and the archived articles are historical.
ENGLISH_ONLY = ("/privacy-policy", "/terms-of-service")

# --- Navigation and calls to action ---------------------------------------
NAV = (
    ("Platform", (
        ("Overview", "/platform"),
        ("Access management", "/platform/access-management"),
        ("Automation", "/platform/automation"),
        ("Visitor access", "/platform/visitor-access"),
    )),
    ("Solutions", (
        ("Property managers", "/solutions/property-managers"),
        ("Integrators", "/solutions/integrators"),
    )),
    ("Products", (
        ("Readers", "/products/readers"),
        ("Compatibility", "/compatibility"),
        ("Certifications", "/certifications"),
    )),
    ("Resources", (
        ("Guides", "/resources#guides"),
        ("Instructions", INSTALLATION_GUIDE),
        ("Insights", "/resources#insights"),
        ("Security and trust", "/security"),
    )),
)
FOOTER = (
    ("Platform", (
        ("Overview", "/platform"),
        ("Access management", "/platform/access-management"),
        ("Automation", "/platform/automation"),
        ("Visitor access", "/platform/visitor-access"),
    )),
    ("Products", (
        ("Readers", "/products/readers"),
        ("Compatibility", "/compatibility"),
        ("Certifications", "/certifications"),
        ("Apps", "/apps-and-chatbot"),
        ("Find your setup", "/find-your-setup"),
    )),
    ("Instructions", tuple((label, path) for path, label in INSTRUCTION_PATHS.items())),
    ("Resources", (
        ("Guides", "/resources#guides"),
        ("Property managers", "/solutions/property-managers"),
        ("Integrators", "/solutions/integrators"),
        ("Security and trust", "/security"),
    )),
    ("Company", (
        ("About", "/about"),
        ("Contact", "/contact"),
        ("Become a partner", "/contact?interest=partner"),
        ("Privacy Policy", "/privacy-policy"),
        ("Terms of Service", "/terms-of-service"),
    )),
)
CTA = {
    "explore": ("Explore the platform", "/platform"),
    "setup": ("Find your setup", "/find-your-setup"),
    "project": ("Discuss your project", "/contact?interest=project"),
    "compatibility": ("Check compatibility", "/compatibility"),
    "partner": ("Become a partner", "/contact?interest=partner"),
    "admin": ("Admin Panel", "/adminpanel"),
    "guides": ("Read the guides", "/resources#guides"),
}

# --- Enquiry form ---------------------------------------------------------
ENQUIRY_TYPES = (
    ("project", "Project planning"),
    ("compatibility", "Product compatibility"),
    ("integration", "Integration"),
    ("partner", "Partnership"),
    ("walkthrough", "Product walkthrough"),
    ("other", "Other"),
)
ROLES = (
    ("property_manager", "Property manager"),
    ("integrator", "Installer or integrator"),
    ("owner", "Building owner"),
    ("other", "Other"),
)
SITES = (
    ("one", "1 site"),
    ("two_to_ten", "2 to 10 sites"),
    ("eleven_plus", "11 or more sites"),
)
DOORS = (
    ("one_to_five", "1 to 5 doors"),
    ("six_to_twentyfive", "6 to 25 doors"),
    ("twentysix_plus", "26 or more doors"),
)
CONNECTIONS = (
    ("wifi", "Wi-Fi"),
    ("cellular", "Cellular"),
    ("both", "Both"),
    ("unsure", "Not sure yet"),
)
INTERESTS = (
    ("cards", "Physical cards"),
    ("wallets", "Wallet credentials"),
    ("visitors", "Visitor access"),
    ("automation", "Automation"),
    ("cameras", "Cameras"),
)
# ``/contact?interest=...``: the enquiry type it preselects and the interests it ticks.
INTEREST_PARAM = {
    "project": ("project", ()),
    "compatibility": ("compatibility", ()),
    "technical": ("compatibility", ()),
    "integration": ("integration", ()),
    "partner": ("partner", ()),
    "walkthrough": ("walkthrough", ()),
    "visitor": ("project", ("visitors",)),
    "automation": ("project", ("automation",)),
}
FIELD_LIMITS = {
    "name": 120, "email": 254, "company": 160, "region": 100, "details": 4000, "phone": 40,
    "utm_source": 120, "utm_medium": 120, "utm_campaign": 120,
}

# --- Setup guide ------------------------------------------------------------
# Deterministic rules, evaluated in Python for the no-JS result and in
# static/src/js/setup_guide.js (the same data, serialised into the page).
# ``when`` maps a field to the values that trigger the rule; an empty
# ``when`` always applies; ``interests`` matches when any listed one is chosen.
SETUP_ROLES = ROLES[:3]
SETUP_INTERESTS = INTERESTS[:4]
SETUP_CONNECTION_ADVICE = {
    "wifi": "Start by checking Wi-Fi coverage and network requirements at each planned reader location.",
    "cellular": "Discuss LTE coverage, SIM provisioning and the reader model for your installation.",
    "both": "We’ll help compare connection options and site requirements.",
    "unsure": "We’ll help compare connection options and site requirements.",
}
SETUP_LINKS = {
    "lte_wifi": ("LTE or Wi-Fi: what fits your site?", "/resources/lte-vs-wifi-access-control"),
    "readers": ("Compare reader configurations", "/products/readers"),
    "access_management": ("Access management across sites", "/platform/access-management"),
    "property_managers": ("Access control for property teams", "/solutions/property-managers"),
    "integrators": ("Installer and integrator workflow", "/solutions/integrators"),
    "installation": ("Installation and connection guide", "/guide-for-usage-and-installation"),
    "cards": ("Which NFC cards can SmartphoneKey program?", "/resources/mifare-classic-desfire-ev3"),
    "compatibility": ("Card and device compatibility", "/compatibility"),
    "visitors": ("Visitor access", "/platform/visitor-access"),
    "automation": ("Automation with connected devices", "/platform/automation"),
    "matter": ("Matter and Thread for access control", "/resources/matter-thread-access-control"),
    "offline": ("What happens when a reader goes offline?", "/resources/access-control-when-offline"),
}
SETUP_RULES = (
    {"when": {}, "item": "List each door with its existing lock hardware, power supply and planned reader position.",
     "links": ()},
    {"when": {"connection": ("wifi", "both", "unsure")},
     "item": "Check Wi-Fi coverage and the network settings the reader will need at every planned location.",
     "links": ("lte_wifi",)},
    {"when": {"connection": ("cellular", "both", "unsure")},
     "item": "Check cellular coverage at every planned location and who will provide the SIM and service.",
     "links": ("lte_wifi", "readers")},
    {"when": {"sites": ("two_to_ten", "eleven_plus")},
     "item": "Decide how each site is organised and who manages it locally.",
     "links": ("access_management",)},
    {"when": {"doors": ("six_to_twentyfive", "twentysix_plus")},
     "item": "Group the doors by building and network area before choosing the connection for each location.",
     "links": ("offline",)},
    {"when": {"role": ("property_manager",)},
     "item": "Map your resident, staff and contractor groups to the doors they need.",
     "links": ("property_managers",)},
    {"when": {"role": ("owner",)},
     "item": "Decide who will issue and revoke access for your property day to day.",
     "links": ("access_management",)},
    {"when": {"role": ("integrator",)},
     "item": "Plan the installation, the customer handover and who supports the site afterwards.",
     "links": ("integrators", "installation")},
    {"when": {"interests": ("cards",)},
     "item": "Confirm the card family and credential format. The documented programming workflows cover "
             "MIFARE Classic and MIFARE DESFire EV3.",
     "links": ("cards",)},
    {"when": {"interests": ("wallets",)},
     "item": "Check the phone, operating system and account requirements for wallet credentials.",
     "links": ("compatibility",)},
    {"when": {"interests": ("visitors",)},
     "item": "Decide the contact path a visitor should follow at each entrance.",
     "links": ("visitors",)},
    {"when": {"interests": ("automation",)},
     "item": "List the devices each workflow needs and the capabilities they report. Current scenarios use "
             "one hub and its commissioned devices.",
     "links": ("automation", "matter")},
)
# The compact tool in the home hero: two choices, frozen copy from the design reference.
HOME_SITE_CHOICES = (
    ("property", "One property"),
    ("portfolio", "Several sites"),
    ("partner", "Customer installations"),
)
HOME_SITE_COPY = {
    "property": "Organise people and permissions around your property.",
    "portfolio": "Keep each site and its local responsibilities organised.",
    "partner": "Plan installation, customer handover and ongoing support.",
}
HOME_CONNECTION_COPY = {
    "wifi": "Start with Wi-Fi coverage at each reader location.",
    "cellular": "Review LTE coverage and SIM provisioning for the installation.",
    "both": "Compare Wi-Fi readiness with LTE coverage before choosing hardware.",
    "unsure": "Review connection options and site requirements before choosing hardware.",
}
# The home choice, carried into the full guide's own fields.
HOME_SITE_TO_SETUP = {
    "property": {"sites": "one"},
    "portfolio": {"sites": "two_to_ten"},
    "partner": {"role": "integrator"},
}

# --- The Webflow site's URLs ---------------------------------------------------
# Every URL of the 34-page snapshot. ``retain`` keeps the URL in the 2.0
# shell, ``redirect`` answers a permanent redirect to the equivalent page,
# ``baseline`` leaves the URL to the AP-428 module unchanged.
LEGACY_ROUTES = {
    "/": ("retain", "/"),
    "/404": ("not_found", None),
    "/adminpanel": ("baseline", None),  # the portal entry redirect stays as configured
    "/apps-and-chatbot": ("retain", "/apps-and-chatbot"),
    "/blog": ("redirect", "/resources"),
    "/certifications": ("retain", "/certifications"),
    "/contact": ("retain", "/contact"),
    "/facility-services": ("redirect", "/solutions/property-managers"),
    "/features": ("redirect", "/platform"),
    "/guide-for-usage-and-installation": ("instruction_site", None),
    "/how-it-works": ("redirect", "/platform"),
    "/intercom-solution": ("redirect", "/platform/visitor-access"),
    "/privacy-policy": ("retain", "/privacy-policy"),
    "/products/smartphonekey-reader-1": ("redirect", "/products/readers"),
    # Prices and partner terms stay on the existing noindex page until the
    # programme is verified; the 2.0 site neither links nor republishes it.
    "/referral-program": ("baseline", None),
    "/security-professionals": ("redirect", "/solutions/integrators"),
    "/smart-home-integrators": ("redirect", "/solutions/integrators"),
    "/team": ("redirect", "/about"),
    "/terms-of-service": ("retain", "/terms-of-service"),
}
LEGACY_POSTS = (
    "how-smartphonekey-enhances-security-for-your-property",
    "matter-standard-the-key-to-a-seamless-smart-home",
    "smart-home-trends-2025-the-future-of-secure-and-connected-living",
    "smartphonekey-official-launch",
    "the-future-of-keyless-entry-why-its-time-to-upgrade-to-smartphonekey",
    "welcome-to-smartphonekey-your-affordable-access-to-a-keyless-future",
)
LEGACY_TEAM = (
    "alex-sydorenko", "denys-merkulov", "ioannis-mavridis", "kate-vasylenko", "kostiantyn-dolzhenko",
    "lana-ostapenko", "oleksii-andrieiev", "vadym-sydorenko", "vitalii-dolzhenko",
)


def route_path(path):
    """The path without its fragment and query (for matching the current page)."""
    return path.split("#", 1)[0].split("?", 1)[0]


def canonical_url(path):
    return ORIGIN + path


def public_paths():
    """Indexable 2.0 routes with their own templates (for the sitemap and crawlers)."""
    return [path for path, route in ROUTES.items() if route.get("index", True)]


def lang_url(path, url_code):
    """``path`` in the language ``url_code`` (English has no prefix)."""
    if url_code == DEFAULT_LANG:
        return path
    return "/" + url_code + ("" if path == "/" else path)


def translatable_strings():
    """Every English string of this module the pages show, for the catalogues.

    The ``.po`` files carry them as Python code terms; tests check that each
    language translates every one of them."""
    strings = []
    for route in ROUTES.values():
        strings += [route["title"], route["description"], route["label"]]
    for group, links in NAV + FOOTER:
        strings.append(group)
        strings += [label for label, _path in links]
    strings += [label for label, _path in CTA.values()]
    strings += list(INSTRUCTION_PATHS.values())
    for choices in (ENQUIRY_TYPES, ROLES, SITES, DOORS, CONNECTIONS, INTERESTS, HOME_SITE_CHOICES):
        strings += [label for _key, label in choices]
    strings += list(SETUP_CONNECTION_ADVICE.values())
    strings += [rule["item"] for rule in SETUP_RULES]
    strings += [label for label, _path in SETUP_LINKS.values()]
    strings += list(HOME_SITE_COPY.values()) + list(HOME_CONNECTION_COPY.values())
    strings += list(EXTRA_STRINGS)
    seen, unique = set(), []
    for text in strings:
        if text not in seen:
            seen.add(text)
            unique.append(text)
    return unique


# The groups of the Guides section on /resources.
GUIDE_GROUPS = (
    ("getting_started", "Getting started"),
    ("cards_devices", "Cards and devices"),
    ("networks_automation", "Networks and automation"),
    ("operating", "Operating your system"),
)

# Strings built in Python outside the tables above.
EXTRA_STRINGS = (
    "Home",
    "Page not found",
    "Getting started",
    "Cards and devices",
    "Networks and automation",
    "Operating your system",
    "Page not found | SmartphoneKey",
    "The page you asked for is not on the SmartphoneKey website.",
    "%(name)s, %(job)s | SmartphoneKey",
    "%(name)s is %(job)s at SmartphoneKey.",
    "Read",
    "Program",
    "Control",
    "Connect",
    "Manage",
    "Enter your name, between 2 and 120 characters.",
    "Enter a valid email address.",
    "Choose what you would like help with.",
    "Use 160 characters or fewer for the company.",
    "Use 100 characters or fewer for the country or region.",
    "Use 4,000 characters or fewer for the project details.",
    "Enter a phone number using digits, spaces and + ( ) - only, up to 40 characters.",
    "Choose one of the listed options.",
    "This form has expired. Reload the page and send it again.",
)
