#!/usr/bin/env python3
"""Build spk_website_v2/i18n from Odoo's term export and the translations.

1. Export the template from a test database with the module installed:
       odoo -d <db> --i18n-export=spk_website_v2.pot --modules=spk_website_v2
2. Run this script. It writes ``i18n/spk_website_v2.pot`` (Odoo's terms plus the
   English strings of site_content.py as Python code terms) and one ``.po`` per
   site language. Translations come from the existing ``.po`` files, or from
   ``--translations <dir>`` (``<lang>.json`` keyed by the ids of ``--source``).

   Terms of the legal pages, the archived articles, the team biographies and
   the backend stay untranslated on purpose: those pages are English-only.

    python i18n_build.py --pot export.pot --addon ../addons/spk_website_v2
        [--source source.json --translations <dir>]

Needs polib.
"""

import argparse
import importlib.util
import json
from pathlib import Path

import polib

LANGS = {"fr": "French", "de": "German", "es": "Spanish", "uk": "Ukrainian"}
CODE_REF = ("code:addons/spk_website_v2/site_content.py", "0")
ENGLISH_ONLY_REFS = (
    "spk_website_v2.page_privacy_policy", "spk_website_v2.page_terms_of_service", ".post_",
    "spk.website.team.member,bio",
)


def load_site_content(addon):
    spec = importlib.util.spec_from_file_location("site_content", addon / "site_content.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_public(entry):
    """A term the public 2.0 pages show in every language."""
    for ref, _line in entry.occurrences:
        if ref.startswith("code:addons/spk_website_v2/site_content.py"):
            return True
        if any(marker in ref for marker in ENGLISH_ONLY_REFS):
            continue
        if ref.startswith("model_terms:ir.ui.view,arch_db:spk_website_v2."):
            view = ref.split(":", 2)[2]
            if not view.startswith(("spk_website_v2.view_", "spk_website_v2.crm_lead_view")):
                return True
        if ref.startswith(("model:spk.website.resource", "model_terms:spk.website.resource",
                           "model:spk.website.compatibility", "model:spk.website.team.member,job_title",
                           "model:spk.website.team.member,photo_alt")):
            return True
    return False


def build_template(pot_path, content):
    pot = polib.pofile(str(pot_path))
    by_id = {entry.msgid: entry for entry in pot}
    for text in content.translatable_strings():
        entry = by_id.get(text)
        if entry is None:
            entry = polib.POEntry(msgid=text, msgstr="", comment="module: spk_website_v2")
            pot.append(entry)
            by_id[text] = entry
        if CODE_REF not in entry.occurrences:
            entry.occurrences.append(CODE_REF)
        if "odoo-python" not in entry.comment:
            entry.comment = entry.comment + "\nodoo-python"
        if "%(" in text and "python-format" not in entry.flags:
            entry.flags.append("python-format")
    return pot


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pot", type=Path, required=True)
    parser.add_argument("--addon", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--translations", type=Path)
    args = parser.parse_args()
    content = load_site_content(args.addon)
    pot = build_template(args.pot, content)
    out = args.addon / "i18n"
    out.mkdir(exist_ok=True)
    pot.metadata["Project-Id-Version"] = "SmartphoneKey Website 2.0"
    pot.save(str(out / "spk_website_v2.pot"))
    ids = dict(json.loads(args.source.read_text(encoding="utf-8"))) if args.source else {}
    for code, name in LANGS.items():
        previous = {}
        if (out / ("%s.po" % code)).exists():
            previous = {entry.msgid: entry.msgstr for entry in polib.pofile(str(out / ("%s.po" % code)))}
        if args.translations:
            by_id = json.loads((args.translations / ("%s.json" % code)).read_text(encoding="utf-8"))
            previous.update({ids[key]: value for key, value in by_id.items() if key in ids})
        po = polib.POFile()
        po.metadata = dict(pot.metadata, Language=code, **{"Content-Type": "text/plain; charset=UTF-8"})
        missing = 0
        for entry in pot:
            copy = polib.POEntry(msgid=entry.msgid, msgstr="", occurrences=list(entry.occurrences),
                                 comment=entry.comment, flags=list(entry.flags))
            if is_public(entry):
                copy.msgstr = previous.get(entry.msgid, "")
                missing += not copy.msgstr
            po.append(copy)
        po.save(str(out / ("%s.po" % code)))
        print("%s (%s): %d terms, %d public terms untranslated" % (code, name, len(po), missing))


if __name__ == "__main__":
    main()
