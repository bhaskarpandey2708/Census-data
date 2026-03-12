#!/usr/bin/env python3
"""Scrape downloadable census-related file links from one or more seed pages."""

from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".zip", ".pdf"}
DEFAULT_OUTPUT = Path("data/raw/census2011/discovered_links.csv")
USER_AGENT = "Mozilla/5.0 (compatible; CensusDataBot/1.0)"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href")
        if href:
            self._current_href = href
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href is not None:
            label = " ".join(part.strip() for part in self._current_text if part.strip())
            self.links.append((self._current_href, label))
            self._current_href = None
            self._current_text = []


def normalize_link(base_url: str, href: str) -> str:
    return urljoin(base_url, href.strip())


def extension_of(url: str) -> str:
    path = urlparse(url).path.lower()
    idx = path.rfind(".")
    return path[idx:] if idx != -1 else ""


def fetch_html(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def scrape_links(seed_urls: list[str], timeout: int) -> tuple[list[tuple[str, str]], list[str]]:
    results: set[tuple[str, str]] = set()
    warnings: list[str] = []

    for seed in seed_urls:
        try:
            html = fetch_html(seed, timeout)
        except Exception as exc:
            warnings.append(f"failed_seed={seed} reason={exc}")
            continue

        parser = LinkParser()
        parser.feed(html)
        for href, text in parser.links:
            link = normalize_link(seed, href)
            if extension_of(link) in ALLOWED_EXTENSIONS:
                results.add((link, text))

    return sorted(results, key=lambda x: x[0]), warnings


def write_csv(rows: list[tuple[str, str]], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["url", "label"])
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed-url",
        action="append",
        dest="seed_urls",
        required=True,
        help="Seed page URL to parse for downloadable links. Repeatable.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output CSV path for discovered links.")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds (default: 30).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, warnings = scrape_links(seed_urls=args.seed_urls, timeout=args.timeout)
    output = Path(args.output)
    write_csv(rows, output)
    print(f"Discovered {len(rows)} download links -> {output}")
    for warning in warnings:
        print(f"[WARN] {warning}")


if __name__ == "__main__":
    main()
