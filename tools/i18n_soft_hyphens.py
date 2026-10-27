#!/usr/bin/env python3
"""Add soft hyphens (U+00AD) to the long words of the translated page text.

Display headings in German, Spanish, Ukrainian and French can hold words wider
than a phone screen ("Zutrittskontrolle"). Browsers only hyphenate with a
dictionary for the language, which many do not have, so the break points are
written into the text: they are invisible unless a word has to break.

Only paragraph-length page and guide text is touched (template terms of 80
characters or more, guide bodies, compatibility rows), and only words of 16
characters or more. Headings, labels, titles, meta descriptions and other
strings the code uses, product names, markup and URLs are left alone: the
design sets headings to ``hyphens: manual`` and relies on their width budget
instead. Run after i18n_build.py; it is idempotent.

    python i18n_soft_hyphens.py --addon ../addons/spk_website_v2

Needs polib and pyphen.
"""

import argparse
import re
from pathlib import Path

import polib
import pyphen

SHY = "­"
LANGS = {"de": ("de_DE", 16), "es": ("es", 16), "fr": ("fr", 16), "uk": ("uk_UA", 16)}
# Headings carry no soft hyphens (DESIGN.md): only paragraph-length terms are touched.
MIN_TERM_LENGTH = 80
TEXT_REFS = ("model_terms:ir.ui.view,arch_db:", "model_terms:spk.website.resource,body:",
             "model:spk.website.resource,name:", "model:spk.website.compatibility,")
TAG_OR_TEXT = re.compile(r"(<[^>]+>)")
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def hyphenate_text(text, dictionary, minimum):
    def word(match):
        token = match.group(0)
        if len(token) < minimum or any(char.isupper() for char in token[1:]):
            return token  # short, or a product name such as SmartphoneKey / DESFire
        return dictionary.inserted(token, hyphen=SHY)
    parts = TAG_OR_TEXT.split(text)
    return "".join(part if part.startswith("<") else WORD.sub(word, part) for part in parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--addon", type=Path, required=True)
    args = parser.parse_args()
    for code, (dictionary_lang, minimum) in LANGS.items():
        dictionary = pyphen.Pyphen(lang=dictionary_lang, left=3, right=3)
        path = args.addon / "i18n" / ("%s.po" % code)
        po = polib.pofile(str(path))
        changed = 0
        for entry in po:
            refs = [ref for ref, _line in entry.occurrences]
            if not entry.msgstr or any(ref.startswith("code:") for ref in refs):
                continue
            if not any(ref.startswith(TEXT_REFS) for ref in refs):
                continue
            if len(entry.msgid) < MIN_TERM_LENGTH:
                continue  # a heading, label or short line: no soft hyphens
            new = hyphenate_text(entry.msgstr.replace(SHY, ""), dictionary, minimum)
            if new != entry.msgstr:
                entry.msgstr = new
                changed += 1
        po.save(str(path))
        print("%s: %d terms hyphenated" % (code, changed))


if __name__ == "__main__":
    main()
