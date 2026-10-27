#!/usr/bin/env python3
"""Mechanical checks of one translation catalogue of spk_website_v2.

Reports, per language: public terms still untranslated, placeholder and HTML
tag mismatches between msgid and msgstr, product names misspelt, forbidden
wording (the claim register's limits), msgstr identical to msgid where the
English contains letters (a sign of an untranslated string), and leftover
soft hyphens in short terms (headings). Exit code 1 when anything blocking is
found (untranslated public terms, placeholder or tag mismatches, forbidden
words).

    python i18n_check.py --addon ../addons/spk_website_v2 --lang uk [--verbose]

Needs polib. The notion of "public term" is the one of i18n_build.py.
"""

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import polib

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("i18n_build", HERE / "i18n_build.py")
i18n_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i18n_build)

PLACEHOLDER = re.compile(r"%\([a-z_]+\)s|%s|%d")
TAG = re.compile(r"</?([a-zA-Z0-9]+)[^>]*>")
PRODUCT_NAMES = ("SmartphoneKey", "Admin Panel", "MIFARE Classic", "MIFARE DESFire EV3", "Apple Wallet", "Google Wallet",
                 "Wi-Fi", "LTE", "Matter", "Thread", "ChatGPT", "Scenario Builder", "AI Concierge")
MISSPELLINGS = {
    re.compile(r"Smartphone ?key(?!\w)", re.I): "SmartphoneKey",
    re.compile(r"\bWiFi\b|\bWifi\b|\bwi-fi\b|\bWIFI\b"): "Wi-Fi",
    re.compile(r"\bDesfire\b|\bDESFIRE\b"): "DESFire",
    re.compile(r"\bMifare\b"): "MIFARE",
    re.compile(r"\bEV ?3\b(?<!EV3)"): "EV3",
}
FORBIDDEN = (
    (re.compile(r"\b80\s?(m|м|metres|meters|Meter|mètres|metros|метрів)\b", re.I), "a link distance"),
    (re.compile(r"\bEV1\b|\bEV2\b"), "a DESFire generation other than EV3"),
    (re.compile(r"\b(1K|4K|2K|8K)\b"), "a card memory size"),
    (re.compile(r"\$\s?\d|€\s?\d|£\s?\d|₴\s?\d"), "a price"),
)
# Words that must not appear translated as a third-party programmer (C05).
PROGRAMMER = {
    "fr": re.compile(r"programmateur|dispositif de programmation|appareil de programmation|matériel de programmation", re.I),
    "de": re.compile(r"Programmiergerät|Programmierhardware|Programmierger", re.I),
    "es": re.compile(r"programador|dispositivo de programación|hardware de programación", re.I),
    "uk": re.compile(r"програматор|пристр[іо][йя][^ ]* програмування|обладнання для програмування", re.I),
}
LATIN_WORD = re.compile(r"[A-Za-z]{4,}")
CYRILLIC = re.compile(r"[Ѐ-ӿ]")


def main():
    # Windows consoles default to a legacy code page; the report carries every script.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--addon", type=Path, required=True)
    parser.add_argument("--lang", required=True, choices=sorted(i18n_build.LANGS))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    po = polib.pofile(str(args.addon / "i18n" / ("%s.po" % args.lang)))
    blocking, warnings = [], []
    public = [entry for entry in po if i18n_build.is_public(entry)]
    for entry in public:
        if not entry.msgstr:
            blocking.append(("untranslated", entry.msgid))
            continue
        if sorted(PLACEHOLDER.findall(entry.msgid)) != sorted(PLACEHOLDER.findall(entry.msgstr)):
            blocking.append(("placeholders", entry.msgid))
        if sorted(t.lower() for t in TAG.findall(entry.msgid)) != sorted(t.lower() for t in TAG.findall(entry.msgstr)):
            blocking.append(("html tags", entry.msgid))
        for pattern, what in FORBIDDEN:
            if pattern.search(entry.msgstr):
                blocking.append(("forbidden: " + what, entry.msgstr[:120]))
        if PROGRAMMER[args.lang].search(entry.msgstr):
            blocking.append(("third-party programmer wording (C05)", entry.msgstr[:140]))
        for pattern, correct in MISSPELLINGS.items():
            if pattern.search(entry.msgstr) and not pattern.search(entry.msgid):
                warnings.append(("spelling, expected %s" % correct, entry.msgstr[:120]))
        for name in PRODUCT_NAMES:
            if name in entry.msgid and name not in entry.msgstr and name not in ("Matter", "Thread", "LTE"):
                warnings.append(("product name %s missing" % name, entry.msgstr[:120]))
        if entry.msgstr == entry.msgid and LATIN_WORD.search(entry.msgid) and len(entry.msgid) > 12:
            warnings.append(("identical to English", entry.msgid[:120]))
        if args.lang == "uk" and not CYRILLIC.search(entry.msgstr) and LATIN_WORD.search(entry.msgid) and len(entry.msgid) > 25:
            warnings.append(("no Cyrillic in Ukrainian string", entry.msgstr[:120]))
        if "­" in entry.msgstr and len(entry.msgid) < 80:
            warnings.append(("soft hyphen in a short term (heading?)", entry.msgstr[:120]))
    print("%s: %d public terms, %d translated" % (args.lang, len(public), sum(1 for e in public if e.msgstr)))
    for kind, text in blocking:
        print("BLOCKING %s: %s" % (kind, text))
    shown = warnings if args.verbose else warnings[:40]
    for kind, text in shown:
        print("warning %s: %s" % (kind, text))
    if len(warnings) > len(shown):
        print("... %d more warnings (--verbose)" % (len(warnings) - len(shown)))
    print("blocking: %d, warnings: %d" % (len(blocking), len(warnings)))
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
