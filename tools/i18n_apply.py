#!/usr/bin/env python3
"""Fill translations into the four catalogues from a JSON file.

The file maps each English msgid to its translations::

    {"Explore the platform": {"fr": "...", "de": "...", "es": "...", "uk": "..."}}

Only entries whose msgid exists in the catalogue are touched; an existing
translation is replaced only with ``--overwrite``. Afterwards the script lists
the public entries that are still empty (the notion of "public" is the one of
i18n_build.py), so the caller knows what remains.

    python i18n_apply.py --addon ../addons/spk_website_v2 --translations file.json [--overwrite]

Needs polib.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import polib

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("i18n_build", HERE / "i18n_build.py")
i18n_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i18n_build)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--addon", type=Path, required=True)
    parser.add_argument("--translations", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    table = json.loads(args.translations.read_text(encoding="utf-8"))
    for lang in sorted(i18n_build.LANGS):
        path = args.addon / "i18n" / ("%s.po" % lang)
        po = polib.pofile(str(path))
        filled, unknown = 0, []
        by_id = {entry.msgid: entry for entry in po}
        for msgid, translations in table.items():
            entry = by_id.get(msgid)
            if entry is None:
                unknown.append(msgid)
                continue
            if entry.msgstr and not args.overwrite:
                continue
            if translations.get(lang):
                entry.msgstr = translations[lang]
                filled += 1
        po.save(str(path))
        empty = [entry.msgid for entry in po if i18n_build.is_public(entry) and not entry.msgstr]
        print("%s: %d filled, %d public terms still empty, %d msgids not in the catalogue" % (lang, filled, len(empty), len(unknown)))
        for msgid in empty:
            print("  empty: %s" % msgid[:110])
        for msgid in unknown:
            print("  unknown: %s" % msgid[:110])


if __name__ == "__main__":
    main()
