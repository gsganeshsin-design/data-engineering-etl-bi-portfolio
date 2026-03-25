"""Sample ETL reconciliation utility.

Purpose:
- Validate source and target extracts
- Compare row counts and control totals
- Flag missing IDs and duplicates
- Produce output reports for audit/review
"""
from __future__ import annotations

from pathlib import Path
import csv
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "sample_data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

SOURCE_FILE = DATA_DIR / "source_sales.csv"
TARGET_FILE = DATA_DIR / "target_sales.csv"
REQUIRED_COLUMNS = ["sale_id", "customer_id", "sale_date", "amount"]


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_columns(rows: list[dict[str, str]], required_columns: list[str]) -> list[str]:
    if not rows:
        return ["File is empty"]
    actual = set(rows[0].keys())
    missing = [col for col in required_columns if col not in actual]
    return missing


def find_duplicates(rows: list[dict[str, str]], key: str) -> list[str]:
    counts = Counter(row[key] for row in rows)
    return [k for k, v in counts.items() if v > 1]


def total_amount(rows: list[dict[str, str]]) -> float:
    return round(sum(float(row["amount"]) for row in rows), 2)


def write_csv(file_path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_rows = read_csv(SOURCE_FILE)
    target_rows = read_csv(TARGET_FILE)

    source_missing = validate_columns(source_rows, REQUIRED_COLUMNS)
    target_missing = validate_columns(target_rows, REQUIRED_COLUMNS)

    if source_missing or target_missing:
        raise ValueError(
            f"Column validation failed. Source missing: {source_missing}, Target missing: {target_missing}"
        )

    source_ids = {row["sale_id"] for row in source_rows}
    target_ids = {row["sale_id"] for row in target_rows}

    missing_in_target = sorted(source_ids - target_ids)
    extra_in_target = sorted(target_ids - source_ids)
    duplicate_ids = find_duplicates(target_rows, "sale_id")

    exceptions: list[dict[str, str]] = []
    for sale_id in missing_in_target:
        exceptions.append({"issue_type": "MISSING_IN_TARGET", "sale_id": sale_id})
    for sale_id in extra_in_target:
        exceptions.append({"issue_type": "EXTRA_IN_TARGET", "sale_id": sale_id})
    for sale_id in duplicate_ids:
        exceptions.append({"issue_type": "DUPLICATE_IN_TARGET", "sale_id": sale_id})

    if exceptions:
        write_csv(OUTPUT_DIR / "exceptions.csv", exceptions, ["issue_type", "sale_id"])

    summary = [
        {"metric": "source_row_count", "value": str(len(source_rows))},
        {"metric": "target_row_count", "value": str(len(target_rows))},
        {"metric": "source_amount_total", "value": f"{total_amount(source_rows):.2f}"},
        {"metric": "target_amount_total", "value": f"{total_amount(target_rows):.2f}"},
        {"metric": "missing_in_target", "value": str(len(missing_in_target))},
        {"metric": "extra_in_target", "value": str(len(extra_in_target))},
        {"metric": "duplicate_ids_in_target", "value": str(len(duplicate_ids))},
    ]
    write_csv(OUTPUT_DIR / "reconciliation_summary.csv", summary, ["metric", "value"])
    print("Reconciliation completed. Check output folder.")


if __name__ == "__main__":
    main()
