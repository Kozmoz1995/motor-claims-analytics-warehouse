"""Command-line entrypoint for extraction and sample quality validation."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .extract import paginated_extract, write_jsonl
from .quality import validate_crash


def validate_file(path: Path) -> dict[str, object]:
    errors: Counter[str] = Counter()
    seen: set[str] = set()
    total = valid = 0
    with path.open(encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            total += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                errors["invalid_json"] += 1
                continue
            collision_id = record.get("collision_id")
            if collision_id in seen:
                errors["duplicate_collision_id"] += 1
                continue
            result = validate_crash(record)
            if result.valid:
                valid += 1
                seen.add(str(collision_id))
            else:
                errors.update(result.reasons)
    return {
        "total": total,
        "valid": valid,
        "invalid": total - valid,
        "validity_rate": round(valid / total, 4) if total else 0,
        "errors": dict(sorted(errors.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    extract = commands.add_parser("extract")
    extract.add_argument("--dataset", choices=["crashes", "vehicles", "persons"], required=True)
    extract.add_argument("--limit", type=int, default=10_000)
    extract.add_argument("--since")
    extract.add_argument("--output", type=Path, required=True)
    commands.add_parser("validate-sample")
    validate = commands.add_parser("validate")
    validate.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "extract":
        count = write_jsonl(
            paginated_extract(args.dataset, args.limit, since=args.since), args.output, args.dataset
        )
        print(json.dumps({"dataset": args.dataset, "records_written": count}, indent=2))
    else:
        path = Path("data/sample/crashes.jsonl") if args.command == "validate-sample" else args.input
        print(json.dumps(validate_file(path), indent=2))


if __name__ == "__main__":
    main()
