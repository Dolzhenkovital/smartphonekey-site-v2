# -*- coding: utf-8 -*-
"""The ungated setup guide: enum choices in, a planning checklist out.

Deterministic and shared: the controller renders the result for a request
without JavaScript, and static/src/js/setup_guide.js evaluates the same rules
(serialised by ``rules_for_script``) in the browser. No contact details,
prices, hardware quantities or radio distances.
"""

from urllib.parse import urlencode

from . import site_content as content

FIELDS = {
    "role": dict(content.SETUP_ROLES),
    "sites": dict(content.SITES),
    "doors": dict(content.DOORS),
    "connection": dict(content.CONNECTIONS),
}
INTEREST_KEYS = tuple(key for key, _label in content.SETUP_INTERESTS)


def clean_selection(single, interests):
    """Keep only allowlisted enum values. ``single`` maps field -> raw value."""
    selection = {field: single.get(field) for field in FIELDS if single.get(field) in FIELDS[field]}
    chosen = [key for key in INTEREST_KEYS if key in set(interests or ())]
    if chosen:
        selection["interests"] = chosen
    return selection


def _matches(rule, selection):
    for field, values in rule["when"].items():
        chosen = selection.get(field)
        if field == "interests":
            if not set(chosen or ()).intersection(values):
                return False
        elif chosen not in values:
            return False
    return True


def _identity(text, **kwargs):
    return text % kwargs if kwargs else text


def result_for(selection, t=_identity):
    """The planning starting point, or None until a connection is chosen.

    ``t`` translates the texts (rendering.translator); link paths stay
    language-neutral because the page adds the language prefix itself."""
    connection = selection.get("connection")
    if not connection:
        return None
    items, links, seen = [], [], set()
    for rule in content.SETUP_RULES:
        if _matches(rule, selection):
            items.append(t(rule["item"]))
            for key in rule["links"]:
                if key not in seen:
                    seen.add(key)
                    label, path = content.SETUP_LINKS[key]
                    links.append((t(label), path))
    return {
        "advice": t(content.SETUP_CONNECTION_ADVICE[connection]),
        "items": items,
        "links": links,
        "contact_href": contact_href(selection),
    }


def contact_href(selection):
    """``/contact`` with the enum choices prefilled. Never anything personal."""
    params = [("interest", "project")]
    params += [(field, selection[field]) for field in ("role", "sites", "doors", "connection") if selection.get(field)]
    params += [("interests", key) for key in selection.get("interests", ())]
    return "/contact?" + urlencode(params)


def rules_for_script(t=_identity, url_code=content.DEFAULT_LANG):
    """The rules for setup_guide.js, in the visitor's language. Links in a
    script are not rewritten by Odoo, so they carry the language prefix."""
    return {
        "advice": {key: t(text) for key, text in content.SETUP_CONNECTION_ADVICE.items()},
        "rules": [{"when": {field: list(values) for field, values in rule["when"].items()},
                   "item": t(rule["item"]), "links": list(rule["links"])} for rule in content.SETUP_RULES],
        "links": {key: [t(label), content.lang_url(path, url_code)]
                  for key, (label, path) in content.SETUP_LINKS.items()},
        "home": {
            "site": {key: t(text) for key, text in content.HOME_SITE_COPY.items()},
            "connection": {key: t(text) for key, text in content.HOME_CONNECTION_COPY.items()},
            "toSetup": content.HOME_SITE_TO_SETUP,
        },
    }
