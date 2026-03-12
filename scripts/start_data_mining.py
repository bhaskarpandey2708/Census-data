#!/usr/bin/env python3
"""Create an initial mining queue from known Census sources and optional discovered links."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (compatible; CensusDataBot/1.0)"


@dataclass
class SourceRow:
    source_name: str
    category: str
    url: str
    priority: int
    notes: str


def read_registry(path: Path) -> list[SourceRow]:
    rows: list[SourceRow] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                SourceRow(
                    source_name=(row.get("source_name") or "").strip(),
                    category=(row.get("category") or "").strip(),
                    url=(row.get("url") or "").strip(),
                    priority=int((row.get("priority") or "3").strip() or "3"),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return rows


def read_discovered(path: Path) -> list[str]:
    if not path.exists():
        return []
    out: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            url = (row.get("url") or "").strip()
            if url:
                out.append(url)
    return out


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def probe_url(url: str, timeout: int) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urlopen(req, timeout=timeout) as response:
            return "ok", str(getattr(response, "status", "200"))
    except Exception as exc:
        return "warn", str(exc)


def write_queue(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_name",
                "category",
                "url",
                "priority",
                "url_valid",
                "probe_status",
                "probe_detail",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="config/source_registry.csv")
    parser.add_argument("--discovered", default="data/raw/census2011/discovered_links.csv")
    parser.add_argument("--output", default="data/raw/census2011/manifests/mining_queue.csv")
    parser.add_argument("--timeout", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry_rows = read_registry(Path(args.registry))
    discovered_urls = read_discovered(Path(args.discovered))

    queue: list[dict[str, str]] = []
    seen: set[str] = set()

    for row in registry_rows:
        if row.url in seen:
            continue
        seen.add(row.url)
        valid = is_valid_url(row.url)
        probe_status, probe_detail = ("skip", "invalid-url")
        if valid:
            probe_status, probe_detail = probe_url(row.url, args.timeout)

        queue.append(
            {
                "source_name": row.source_name,
                "category": row.category,
                "url": row.url,
                "priority": str(row.priority),
                "url_valid": "yes" if valid else "no",
                "probe_status": probe_status,
                "probe_detail": probe_detail,
                "notes": row.notes,
            }
        )

    for idx, url in enumerate(discovered_urls, start=1):
        if url in seen:
            continue
        seen.add(url)
        valid = is_valid_url(url)
        probe_status, probe_detail = ("skip", "invalid-url")
        if valid:
            probe_status, probe_detail = probe_url(url, args.timeout)

        queue.append(
            {
                "source_name": f"discovered_{idx}",
                "category": "discovered",
                "url": url,
                "priority": "4",
                "url_valid": "yes" if valid else "no",
                "probe_status": probe_status,
                "probe_detail": probe_detail,
                "notes": "Auto-discovered from scraper output",
            }
        )

    queue.sort(key=lambda x: (int(x["priority"]), x["source_name"]))
    output = Path(args.output)
    write_queue(queue, output)
    print(f"Wrote mining queue with {len(queue)} records -> {output}")


if __name__ == "__main__":
    main()
