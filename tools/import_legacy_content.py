#!/usr/bin/env python3
"""One-off import of the Webflow site's retained content into spk_website_v2.

Reads the local Webflow API export and mirror (never their private
submissions), and writes:

* data/website_posts.xml  - the six blog articles kept at /post/<slug>
* data/website_team.xml   - the nine team pages kept at /team/<slug>
* views/legal_pages.xml   - the privacy policy and terms, text unchanged
* static/src/img/...      - web-sized copies of the images they use,
                            the brand mark, the reader photo and the OG card

The generated files are committed and maintained in the module from then on;
run this again only to re-import from a fresh export.

    python import_legacy_content.py --export <export dir> --mirror <mirror/raw dir>
        --handoff <docs/site-v2 dir> --addon <addons/spk_website_v2>

Needs lxml and Pillow.
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from lxml import etree, html as lxml_html
from PIL import Image

SITE = "https://smartphonekey.com"
# Links in the old articles that moved or point at another brand's profiles.
LINK_REWRITES = {
    "https://smartphonekey.com/products/smartphonekey-reader-1": "/products/readers",
    "https://smartphonekey.com/": "/",
    "https://smartphonekey.com": "/",
}
UNLINK_HOSTS = ("mykey.cards", "mykey_cards", "mykey-cards")
ALLOWED_TAGS = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "em", "a", "figure", "img", "blockquote", "br"}
ADVISOR_MARK = "Advisor at SmartphoneKey"


def field(item, key):
    return item["fieldData"].get(key)


def image_ref(value):
    """The Webflow image field arrives as a dict or as its Python repr."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and "fileId" in value:
        match = re.search(r"'fileId': '([0-9a-f]+)'", value)
        return {"fileId": match.group(1)} if match else None
    return None


def save_webp(source, target, max_width, quality=80):
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGBA") if image.mode in ("P", "LA") else image
        if image.width > max_width:
            image = image.resize((max_width, round(image.height * max_width / image.width)), Image.LANCZOS)
        image.save(target, "WEBP", quality=quality, method=6)
        return image.size


def clean_fragment(body_html, local_images, hero_file_id):
    """Webflow rich text -> plain semantic HTML (an lxml <div>)."""
    fragment = lxml_html.fragment_fromstring(body_html, create_parent="div")
    for element in list(fragment.iter()):
        if not isinstance(element.tag, str):
            continue
        for attribute in list(element.attrib):
            if attribute not in ("href", "src", "alt"):
                del element.attrib[attribute]
    for iframe in list(fragment.iter("iframe")):
        src = unquote(iframe.get("src", ""))
        query = parse_qs(urlsplit(src).query)
        video = (query.get("src") or [src])[0]
        match = re.search(r"youtube\.com/embed/([\w-]+)|youtu\.be/([\w-]+)", video)
        container = iframe.getparent()
        while container is not None and container.getparent() is not fragment:
            container = container.getparent()
        replacement = None
        if match:
            replacement = etree.Element("p")
            link = etree.SubElement(replacement, "a", href="https://www.youtube.com/watch?v=%s" % (match.group(1) or match.group(2)))
            link.text = "Watch the video on YouTube"
        target = container if container is not None else iframe
        previous = target.getprevious()
        if replacement is not None and previous is not None and previous.tag == "p" and len(previous)                 and previous[0].get("href") == replacement[0].get("href"):
            replacement = None  # the same video embedded twice
        if replacement is not None:
            target.addprevious(replacement)
        target.getparent().remove(target)
    for figure in list(fragment.iter("figure")):
        image = figure.find(".//img")
        file_id = None
        if image is not None:
            match = re.search(r"/([0-9a-f]{24})_", image.get("src", ""))
            file_id = match.group(1) if match else None
        if not file_id or file_id == hero_file_id or file_id not in local_images:
            figure.getparent().remove(figure)
            continue
        new_figure = etree.Element("figure")
        etree.SubElement(new_figure, "img", src=local_images[file_id], alt="")
        figure.addprevious(new_figure)
        figure.getparent().remove(figure)
    for heading in fragment.xpath("//h2|//h3|//h4"):
        for strong in heading.findall("strong"):
            strong.drop_tag()
    for link in list(fragment.iter("a")):
        href = link.get("href", "")
        if any(host in href for host in UNLINK_HOSTS):
            link.drop_tag()
            continue
        link.set("href", LINK_REWRITES.get(href, href))
    for element in list(fragment.iter()):
        if isinstance(element.tag, str) and element.tag not in ALLOWED_TAGS and element is not fragment:
            element.drop_tag()
    for paragraph in list(fragment.iter("p")):
        if not "".join(paragraph.itertext()).replace("‍", "").strip() and not len(paragraph):
            paragraph.getparent().remove(paragraph)
    return fragment


def to_xml_children(fragment):
    """Serialise an lxml.html fragment as well-formed XML children of a <div>."""
    text = lxml_html.tostring(fragment, encoding="unicode", method="xml")
    return etree.fromstring(text.replace("&nbsp;", " "))


def write_xml(path, root):
    etree.indent(root, space="    ")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = etree.tostring(root, encoding="unicode", pretty_print=True)
    path.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + data, encoding="utf-8", newline="\n")


def add_field(record, name, value=None, **attrs):
    element = etree.SubElement(record, "field", name=name, **attrs)
    if value is not None:
        element.text = value
    return element


def import_posts(export, addon, image_dir):
    posts = json.loads((export / "cms/post/items-live.json").read_text(encoding="utf-8"))
    authors = {item["id"]: field(item, "name")
               for item in json.loads((export / "cms/author/items-live.json").read_text(encoding="utf-8"))}
    files = {path.name.split("_", 1)[0]: path for path in (export / "cms/post/files").iterdir()}
    local_images = {}
    for file_id, path in files.items():
        target = image_dir / "posts" / ("%s.webp" % file_id)
        save_webp(path, target, 1200)
        local_images[file_id] = "/spk_website_v2/static/src/img/posts/%s.webp" % file_id
    root = etree.Element("odoo")
    root.append(etree.Comment(" The Webflow blog articles, kept at /post/<slug> with their original dates and "
                              "author. Imported by tools/import_legacy_content.py; maintained here since. "))
    data = etree.SubElement(root, "data", noupdate="1")
    for index, item in enumerate(sorted(posts, key=lambda post: field(post, "date"), reverse=True), start=1):
        slug = field(item, "slug")
        hero = image_ref(field(item, "main-image"))
        hero_id = hero["fileId"] if hero else None
        record = etree.SubElement(data, "record", id="post_%s" % slug.replace("-", "_"),
                                  model="spk.website.resource")
        seo_title = (field(item, "seo-title") or field(item, "name")).strip()
        if "SmartphoneKey" not in seo_title.split("|")[-1]:
            seo_title += " | SmartphoneKey"
        add_field(record, "kind", "post")
        add_field(record, "sequence", str(index * 10))
        add_field(record, "slug", slug)
        add_field(record, "name", " ".join(field(item, "name").split()))
        add_field(record, "seo_title", " ".join(seo_title.split()))
        add_field(record, "description", (field(item, "seo-description") or field(item, "post-summary")).strip())
        add_field(record, "direct_answer", (field(item, "post-summary") or "").strip())
        add_field(record, "category", "insights")
        if hero_id in local_images:
            add_field(record, "hero_image", local_images[hero_id])
            add_field(record, "hero_alt", "")
        add_field(record, "author_name", authors.get(field(item, "author"), "SmartphoneKey"))
        add_field(record, "published_on", field(item, "date")[:10])
        add_field(record, "is_published", eval="True")
        body = add_field(record, "body", type="html")
        body.append(to_xml_children(clean_fragment(field(item, "post-body"), local_images, hero_id)))
    write_xml(addon / "data/website_posts.xml", root)
    return len(posts)


def import_team(export, addon, image_dir):
    members = json.loads((export / "cms/team/items-live.json").read_text(encoding="utf-8"))
    files = {path.name.split("_", 1)[0]: path for path in (export / "cms/team/files").iterdir()}
    root = etree.Element("odoo")
    root.append(etree.Comment(" The Webflow team pages, kept at /team/<slug>. Roles as published on the "
                              "Webflow site; role_checked_on stays empty until each role is confirmed. "))
    data = etree.SubElement(root, "data", noupdate="1")
    for item in sorted(members, key=lambda member: int(field(member, "order") or 0)):
        slug = field(item, "slug")
        photo = image_ref(field(item, "profile-picture"))
        record = etree.SubElement(data, "record", id="team_%s" % slug.replace("-", "_"),
                                  model="spk.website.team.member")
        bio_html = field(item, "bio") or ""
        add_field(record, "sequence", str(int(field(item, "order") or 0) * 10))
        add_field(record, "slug", slug)
        add_field(record, "name", field(item, "name").strip())
        add_field(record, "job_title", field(item, "job-title").strip())
        add_field(record, "is_advisor", eval=str(ADVISOR_MARK in bio_html))
        if field(item, "linkdin"):
            add_field(record, "linkedin_url", field(item, "linkdin").strip())
        if photo and photo["fileId"] in files:
            target = image_dir / "team" / ("%s.webp" % slug)
            save_webp(files[photo["fileId"]], target, 480)
            add_field(record, "photo", "/spk_website_v2/static/src/img/team/%s.webp" % slug)
            add_field(record, "photo_alt", "Portrait of %s" % field(item, "name").strip())
        add_field(record, "is_published", eval="True")
        body = add_field(record, "bio", type="html")
        body.append(to_xml_children(clean_fragment(bio_html, {}, None)))
    write_xml(addon / "data/website_team.xml", root)
    return len(members)


def legal_sections(mirror_file, drop_list_marker=None):
    """The numbered sections of a Webflow legal page as (title, [nodes])."""
    doc = lxml_html.parse(str(mirror_file)).getroot()
    sections = []
    for heading in doc.xpath("//main//h3"):
        block = heading.getparent().getparent()
        nodes = []
        for child in block:
            if child is heading.getparent():
                continue
            if child.tag == "ul" and drop_list_marker and drop_list_marker in child.text_content():
                continue
            if child.tag in ("p", "ul", "ol"):
                nodes.append(child)
        sections.append((re.sub(r"\s+", " ", heading.text_content()).strip(), nodes))
    return sections


def clean_inline(node):
    clone = lxml_html.fromstring(lxml_html.tostring(node, encoding="unicode"))
    for element in clone.iter():
        for attribute in list(element.attrib):
            if attribute != "href":
                del element.attrib[attribute]
    for element in list(clone.iter()):
        if element.tag not in ("p", "ul", "ol", "li", "strong", "em", "a", "br") and element is not clone:
            element.drop_tag()
    text = lxml_html.tostring(clone, encoding="unicode", method="xml").replace("�", " ")
    return etree.fromstring(text)


def import_legal(mirror, addon):
    root = etree.Element("odoo")
    root.append(etree.Comment(" The Webflow privacy policy and terms of service, text unchanged (an "
                              "installation list that had slipped into the privacy policy's introduction is "
                              "left out). Replace only with a reviewed version. "))
    pages = (
        ("page_privacy_policy", "privacy-policy.html", "Privacy Policy", "Quick start guide"),
        ("page_terms_of_service", "terms-of-service.html", "Terms of Service", None),
    )
    for template_id, filename, title, drop_marker in pages:
        template = etree.SubElement(root, "template", id=template_id, name="SmartphoneKey 2.0: %s" % title)
        call = etree.SubElement(template, "t", {"t-call": "spk_website_v2.layout"})
        wrapper = etree.SubElement(call, "div", {"class": "container spk-document"})
        head = etree.SubElement(wrapper, "t", {"t-call": "spk_website_v2.page_intro"})
        etree.SubElement(head, "t", {"t-set": "heading"}).text = title
        article = etree.SubElement(wrapper, "div", {"class": "spk-prose"})
        for heading, nodes in legal_sections(mirror / filename, drop_marker):
            etree.SubElement(article, "h2").text = heading
            for node in nodes:
                article.append(clean_inline(node))
        email = etree.SubElement(article, "p")
        email.text = "Questions about this page: "
        link = etree.SubElement(email, "a", href="mailto:info@smartphonekey.com")
        link.text = "info@smartphonekey.com"
        link.tail = "."
    write_xml(addon / "views/legal_pages.xml", root)


def brand_assets(handoff, export, image_dir):
    image_dir.mkdir(parents=True, exist_ok=True)
    (image_dir / "brand-mark.png").write_bytes((handoff / "assets/brand-mark.png").read_bytes())
    sizes = {}
    for width in (480, 800):
        sizes[width] = save_webp(handoff / "assets/reader.webp", image_dir / ("reader-%d.webp" % width), width, 82)
    favicon = next((export / "assets/files").glob("*favicon-32x32.png"))
    (image_dir / "favicon-32.png").write_bytes(favicon.read_bytes())
    with Image.open(next((export / "assets/files").glob("*android-chrome-512x512.png"))) as icon:
        icon.convert("RGBA").resize((180, 180), Image.LANCZOS).save(image_dir / "apple-touch-icon.png")
    # Open Graph card: the genuine reader photo and logo on the site's paper colour.
    paper = (247, 244, 241)
    card = Image.new("RGB", (1200, 630), paper)
    with Image.open(handoff / "assets/reader.webp") as reader:
        reader = reader.convert("RGBA")
        reader.thumbnail((560, 560), Image.LANCZOS)
        card.paste(reader, (1200 - reader.width - 80, (630 - reader.height) // 2), reader)
    with Image.open(handoff / "assets/brand-mark.png") as mark:
        mark = mark.convert("RGBA")
        mark.thumbnail((220, 220), Image.LANCZOS)
        card.paste(mark, (120, (630 - mark.height) // 2), mark)
    card.save(image_dir / "og-default.png", optimize=True)
    return sizes


def copy_documents(export, addon):
    target = addon / "static/src/files"
    target.mkdir(parents=True, exist_ok=True)
    documents = {
        "*smartphonekey-ce-red-wifi-reader*.pdf": "ce-red-wifi-reader-spk-ac-wifi-v1-0.pdf",
        "*smartphonekey-ce-red-lte-reader*.pdf": "ce-red-lte-reader-spk-ac-lte-eu-v1-0.pdf",
        "*google-smarttap-2-1-compliance-certificate.jpeg": "google-smart-tap-2-1-compliance-certificate.jpeg",
        "*apple-ecp2-certification-confirmation.docx": "apple-ecp2-certification-confirmation.docx",
    }
    for pattern, name in documents.items():
        source = next((export / "assets/files").glob(pattern))
        (target / name).write_bytes(source.read_bytes())
    return len(documents)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--mirror", type=Path, required=True)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--addon", type=Path, required=True)
    args = parser.parse_args()
    image_dir = args.addon / "static/src/img"
    print("posts:", import_posts(args.export, args.addon, image_dir))
    print("team:", import_team(args.export, args.addon, image_dir))
    import_legal(args.mirror, args.addon)
    print("reader sizes:", brand_assets(args.handoff, args.export, image_dir))
    print("documents:", copy_documents(args.export, args.addon))


if __name__ == "__main__":
    main()
