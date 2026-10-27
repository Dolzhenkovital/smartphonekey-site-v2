#!/usr/bin/env python3
"""A10 check against a running test instance: concurrent submissions of one
enquiry must create exactly one lead.

Opens /contact once (one session, one CSRF token, one submission ID), then
fires the same POST from several threads at once and reports every answer.
Synthetic data only; point it at a local or approved test environment, never
at production.

    python enquiry_concurrency.py http://127.0.0.1:8069 --threads 8
"""

import argparse
import http.cookiejar
import json
import re
import threading
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("base_url")
    parser.add_argument("--threads", type=int, default=8)
    args = parser.parse_args()
    if not re.match(r"^https?://(127\.0\.0\.1|localhost)(:\d+)?$", args.base_url.rstrip("/")):
        raise SystemExit("Refusing to run against anything but a local test instance.")

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    page = opener.open(args.base_url + "/contact").read().decode()
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    submission_id = re.search(r'name="submission_id" value="([0-9a-f]{32})"', page).group(1)
    body = urllib.parse.urlencode({
        "csrf_token": token, "submission_id": submission_id, "source_path": "/contact",
        "name": "Concurrency Test", "email": "concurrency.test@example.com", "enquiry_type": "compatibility",
        "details": "Synthetic concurrency check.",
    }).encode()

    answers = []
    barrier = threading.Barrier(args.threads)

    def send():
        request = urllib.request.Request(args.base_url + "/website/spk/enquiry", data=body,
                                         headers={"Accept": "application/json"})
        barrier.wait()
        try:
            with opener.open(request) as response:
                answers.append((response.status, json.loads(response.read())))
        except urllib.error.HTTPError as error:
            answers.append((error.code, error.read()[:200]))

    threads = [threading.Thread(target=send) for _index in range(args.threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("submission_id", submission_id)
    for answer in sorted(answers, key=str):
        print(answer)


if __name__ == "__main__":
    main()
