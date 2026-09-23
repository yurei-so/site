#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import quote
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

SITE_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://yurei-so.github.io/site"

EXCLUDED_FILES = {
    "404.html",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".github",
    "node_modules",
    "scripts",
}


def page_url(path: Path) -> str:
    relative = path.relative_to(SITE_ROOT)

    # index.html becomes the directory URL.
    if relative.name == "index.html":
        parent = relative.parent.as_posix()

        if parent == ".":
            return f"{BASE_URL}/"

        return f"{BASE_URL}/{quote(parent)}/"

    # Other HTML files keep their filename.
    return f"{BASE_URL}/{quote(relative.as_posix())}"


def should_include(path: Path) -> bool:
    relative = path.relative_to(SITE_ROOT)

    if path.name in EXCLUDED_FILES:
        return False

    return not any(part in EXCLUDED_DIRECTORIES for part in relative.parts)


def main() -> None:
    pages = sorted(
        page_url(path)
        for path in SITE_ROOT.rglob("*.html")
        if should_include(path)
    )

    urlset = Element(
        "urlset",
        {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"},
    )

    for page in pages:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = page

    indent(urlset, space="  ")

    output = SITE_ROOT / "sitemap.xml"
    ElementTree(urlset).write(
        output,
        encoding="utf-8",
        xml_declaration=True,
    )

    print(f"Generated {output} with {len(pages)} pages.")


if __name__ == "__main__":
    main()
