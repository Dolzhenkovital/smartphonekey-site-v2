#!/usr/bin/env python3
"""Check the static review copy before publishing it.

Serves the export under its Pages base path, crawls every page reachable from
the home page and checks: each internal link and asset resolves, each page has
one h1, a title, a description and noindex, the canonical points at the
production origin, and no page carries a session token or local address.
Links to other hosts are listed, not fetched.

    python check_static.py ../preview --base /smartphonekey-site-v2
"""

import argparse
import functools
import http.server
import re
import threading
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from lxml import html as lxml_html

ORIGIN = "https://smartphonekey.com"


class Handler(http.server.SimpleHTTPRequestHandler):
    base = ""

    def translate_path(self, path):
        path = urlsplit(path).path
        if not path.startswith(self.base + "/") and path != self.base:
            return "/nonexistent"
        return super().translate_path(path[len(self.base):] or "/")

    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path)
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    Handler.base = args.base.rstrip("/")
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(args.root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    root = "http://127.0.0.1:%d%s/" % (server.server_address[1], Handler.base)

    seen, queue, problems, external = set(), [root], [], set()
    pages = 0
    while queue:
        url = queue.pop()
        if url in seen:
            continue
        seen.add(url)
        try:
            with urllib.request.urlopen(url) as response:
                body, kind = response.read(), response.headers.get_content_type()
        except urllib.error.HTTPError as error:
            problems.append("%s answered %s" % (url, error.code))
            continue
        if kind != "text/html":
            continue
        pages += 1
        text = body.decode("utf-8")
        doc = lxml_html.fromstring(body)
        refresh = doc.xpath("//meta[@http-equiv='refresh']/@content")
        if refresh:
            queue.append(urljoin(url, refresh[0].split("url=", 1)[1]))
            continue
        path = urlsplit(url).path
        if len(doc.xpath("//h1")) != 1:
            problems.append("%s has %d h1" % (path, len(doc.xpath("//h1"))))
        if not doc.findtext(".//title") or not doc.xpath("//meta[@name='description']/@content"):
            problems.append("%s lacks a title or description" % path)
        if doc.xpath("//meta[@name='robots']/@content") != ["noindex, nofollow"]:
            problems.append("%s is not noindex" % path)
        canonical = doc.xpath("//link[@rel='canonical']/@href")
        if not canonical or not canonical[0].startswith(ORIGIN):
            problems.append("%s canonical %s" % (path, canonical))
        if re.search(r"127\.0\.0\.1:8069|csrf_token: \"", text):
            problems.append("%s carries a local address or token" % path)
        for element in doc.iter():
            if not isinstance(element.tag, str):
                continue
            refs = [element.get(attribute) for attribute in ("href", "src") if element.get(attribute)]
            refs += [part.split()[0] for part in (element.get("srcset") or "").split(",") if part.strip()]
            for ref in refs:
                if element.tag == "link" and element.get("rel") in ("canonical",):
                    continue
                if element.tag == "meta":
                    continue
                target = urljoin(url, ref)
                parts = urlsplit(target)
                if parts.scheme in ("mailto", "tel") or ref.startswith("#"):
                    continue
                if parts.netloc != urlsplit(root).netloc:
                    external.add("%s://%s%s" % (parts.scheme, parts.netloc, parts.path))
                    continue
                queue.append(target.split("#", 1)[0])
    server.shutdown()
    print("checked %d pages and %d URLs" % (pages, len(seen)))
    print("external links (not fetched):")
    for link in sorted(external):
        print("  ", link)
    if problems:
        print("PROBLEMS:")
        for problem in problems:
            print("  ", problem)
        raise SystemExit(1)
    print("no problems")


if __name__ == "__main__":
    main()
