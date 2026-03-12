#!/usr/bin/env python3
"""Download census files from discovered link CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_LINKS = Path("data/raw/census2011/discovered_links.csv")
DEFAULT_OUTDIR = Path("data/raw/census2011/downloads")
USER_AGENT = "Mozilla/5.0 (compatible; CensusDataBot/1.0)"


def filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name
    return name or "downloaded_file"


def read_links(path: Path) -> list[str]:
    urls: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            url = (row.get("url") or "").strip()
            if url:
                urls.append(url)
    return urls


def download(url: str, outdir: Path, timeout: int) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / filename_from_url(url)

    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        with outpath.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 64)
                if not chunk:
                    break
                handle.write(chunk)

    return outpath


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--links-file", default=str(DEFAULT_LINKS), help="CSV of URLs.")
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR), help="Download folder.")
    parser.add_argument("--timeout", type=int, default=90, help="HTTP timeout in seconds.")
    parser.add_argument("--limit", type=int, default=0, help="Max files to download (0 = all).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    links_file = Path(args.links_file)
    outdir = Path(args.outdir)

    urls = read_links(links_file)
    if args.limit > 0:
        urls = urls[: args.limit]

    if not urls:
        print("No URLs found; nothing to download.")
        return

    success = 0
    failures = 0
    for url in urls:
        try:
            path = download(url=url, outdir=outdir, timeout=args.timeout)
            success += 1
            print(f"[OK] {url} -> {path}")
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {url} -> {exc}")

    print(f"Completed. success={success}, failures={failures}")


if __name__ == "__main__":
    main()
