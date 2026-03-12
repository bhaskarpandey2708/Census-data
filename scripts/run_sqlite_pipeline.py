#!/usr/bin/env python3
"""Run a local SQLite demo pipeline using sample staging CSVs."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

DDL_FILES = [
    "sql/ddl/001_geo_dimensions.sql",
    "sql/ddl/002_fact_population_2011.sql",
    "sql/ddl/004_staging_tables.sql",
    "sql/ddl/005_rollup_views.sql",
]
TRANSFORM_FILES = [
    "sql/transforms/tr_population_core.sql",
    "sql/transforms/tr_sc_st.sql",
    "sql/transforms/tr_rural_urban.sql",
    "sql/transforms/tr_religion.sql",
]


def execute_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def load_csv(conn: sqlite3.Connection, table: str, csv_path: Path) -> None:
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        return

    columns = list(rows[0].keys())
    placeholders = ",".join(["?"] * len(columns))
    column_list = ",".join(columns)
    values = [tuple(row[col] for col in columns) for row in rows]
    conn.executemany(
        f"insert into {table} ({column_list}) values ({placeholders})",
        values,
    )


def seed_dimensions(conn: sqlite3.Connection, sample_dir: Path) -> None:
    load_csv(conn, "dim_state", sample_dir / "dim_state.csv")
    load_csv(conn, "dim_district", sample_dir / "dim_district.csv")
    load_csv(conn, "dim_block", sample_dir / "dim_block.csv")
    load_csv(conn, "dim_gram_panchayat", sample_dir / "dim_gram_panchayat.csv")
    load_csv(conn, "dim_village", sample_dir / "dim_village.csv")


def seed_staging(conn: sqlite3.Connection, sample_dir: Path) -> None:
    load_csv(conn, "stg_population_core", sample_dir / "stg_population_core.csv")
    load_csv(conn, "stg_sc_st", sample_dir / "stg_sc_st.csv")
    load_csv(conn, "stg_rural_urban", sample_dir / "stg_rural_urban.csv")
    load_csv(conn, "stg_religion", sample_dir / "stg_religion.csv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="data/curated/census2011.db", help="SQLite DB path")
    parser.add_argument(
        "--sample-dir",
        default="data/staging/sample",
        help="Directory containing sample CSV files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    sample_dir = Path(args.sample_dir)

    conn = sqlite3.connect(db_path)
    try:
        for ddl in DDL_FILES:
            execute_sql_file(conn, Path(ddl))

        seed_dimensions(conn, sample_dir)
        seed_staging(conn, sample_dir)

        for transform in TRANSFORM_FILES:
            execute_sql_file(conn, Path(transform))

        conn.commit()

        row = conn.execute(
            "select geo_level, geo_code, total_population, sc_population, religion_hindu_population "
            "from fact_population_2011 where geo_level='village' and geo_code='V01'"
        ).fetchone()
        print("fact_population_2011 sample row:", row)

        rollup = conn.execute(
            "select state_code, total_population, male_population, female_population "
            "from vw_state_population_2011"
        ).fetchall()
        print("vw_state_population_2011:", rollup)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
