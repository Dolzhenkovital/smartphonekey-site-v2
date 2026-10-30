#!/usr/bin/env python3
"""Derivatives of the real Admin Panel screenshots of 30 October 2026.

Source: ``docs/site-v2/assets/product-ui-2026-10-30/*.jpg`` (authentic browser
captures, see the ASSET-MANIFEST.md beside them). Output: WebP files in
``addons/spk_website_v2/static/src/img/product-ui/`` with stable names and the
pixel width in the name. Only two operations are applied: scaling down (never
up) and rectangular cropping. Nothing is drawn, painted or retouched. Each
crop keeps the complete dialog or panel it is meant to show; the coordinates
are in source pixels and documented here so a reviewer can check them.

    python tools/product_ui_images.py [--source <folder>] [--out <folder>]

Needs Pillow.
"""

import argparse
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
QUALITY = 82

# (source file, output stem, crop box or None, widths to write). Widths above the
# crop's own width are skipped: no upscaling.
DERIVATIVES = (
    # Full dashboard: hero band and the expanded view.
    ("01-admin-dashboard.jpg", "admin-dashboard", None, (2133, 1600, 1200, 800)),
    # Phone close-up: Dashboard title, the complete Give Access button, the first two summary
    # cards, the Locks/Cameras/Matter tabs and the activity rows. The Guest Key button starts at
    # x=1000, the timestamps and the View all button are far right: nothing is cut through.
    ("01-admin-dashboard.jpg", "admin-dashboard-close-up", (56, 56, 992, 896), (936,)),
    # AI Assistant panel at its natural size (422 px; the manifest forbids stretching it).
    ("02-ai-assistant-detail.jpg", "ai-assistant-detail", None, (422,)),
    # The assistant open beside the Dashboard: context image for the access-management page.
    ("02-ai-assistant.jpg", "ai-assistant-context", None, (2370, 1600, 1200)),
    # Assign Key wizard, step 2 of 3, empty recipient: the full capture and the complete dialog
    # with a 24 px margin of its background.
    ("03-assign-access.jpg", "assign-access", None, (1056,)),
    ("03-assign-access.jpg", "assign-access-dialog", (236, 104, 784, 546), (548,)),
    # Devices page filters: shallow overview (the live cards and QR codes were excluded at capture).
    ("04-device-status.jpg", "device-status", None, (2133, 1200)),
    ("04-device-status.jpg", "device-status-close-up", (56, 56, 1460, 328), (1404,)),
    # Recent activity close-up: the left part of the panel (the capture itself is already a crop).
    ("05-recent-activity.jpg", "recent-activity", None, (967,)),
    ("05-recent-activity.jpg", "recent-activity-close-up", (0, 0, 620, 378), (620,)),
    # Guest Key form in Wallet Key mode: full capture and the complete dialog with a 24 px margin.
    ("06-guest-wallet-key.jpg", "guest-wallet-key", None, (1304,)),
    ("06-guest-wallet-key.jpg", "guest-wallet-key-dialog", (313, 116, 861, 748), (548,)),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, default=HERE.parents[1] / "docs/site-v2/assets/product-ui-2026-10-30")
    parser.add_argument("--out", type=Path, default=HERE.parent / "addons/spk_website_v2/static/src/img/product-ui")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    written = []
    for source, stem, box, widths in DERIVATIVES:
        image = Image.open(args.source / source).convert("RGB")
        if box:
            assert box[2] <= image.width and box[3] <= image.height, (source, box, image.size)
            image = image.crop(box)
        for width in widths:
            if width > image.width:
                continue
            copy = image if width == image.width else image.resize(
                (width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            target = args.out / ("%s-%d.webp" % (stem, width))
            copy.save(target, "WEBP", quality=QUALITY, method=6)
            written.append((target.name, copy.width, copy.height, target.stat().st_size))
    for name, width, height, size in written:
        print("%-40s %5d x %4d  %6.1f KB" % (name, width, height, size / 1024))


if __name__ == "__main__":
    main()
