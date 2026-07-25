"""Incremental extraction from NYC Open Data's Socrata API."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DATASETS = {
    "crashes": "h9gi-nx95",
    "vehicles": "bm4k-52h4",
    "persons": "f55k-p6yu",
}
BASE_URL = "https://data.cityofnewyork.us/resource/{dataset_id}.json"


def build_url(dataset: str, limit: int, offset: int = 0, since: str | None = None) -> str:
    if dataset not in DATASETS:
        raise ValueError(f"unknown dataset: {dataset}")
    if not 1 <= limit <= 50_000:
        raise ValueError("limit must be between 1 and 50000")
    params: dict[str, str | int] = {"$limit": limit, "$offset": offset}
    if since:
        datetime.strptime(since, "%Y-%m-%d")
        date_column = "crash_date" if dataset == "crashes" else "crash_date"
        params["$where"] = f"{date_column} >= '{since}T00:00:00.000'"
    return BASE_URL.format(dataset_id=DATASETS[dataset]) + "?" + urlencode(params)


def fetch_records(url: str, app_token: str | None = None) -> list[dict[str, object]]:
    headers = {"User-Agent": "motor-claims-analytics-warehouse/0.1"}
    if app_token:
        headers["X-App-Token"] = app_token
    request = Request(url, headers=headers)
    with urlopen(request, timeout=60) as response:  # nosec: B310 - fixed HTTPS host
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("API response must be a JSON list")
    return payload


def paginated_extract(
    dataset: str, total_limit: int, page_size: int = 10_000, since: str | None = None
) -> Iterator[dict[str, object]]:
    offset = 0
    remaining = total_limit
    while remaining > 0:
        requested = min(page_size, remaining)
        records = fetch_records(build_url(dataset, requested, offset, since))
        if not records:
            break
        yield from records
        offset += len(records)
        remaining -= len(records)
        if len(records) < requested:
            break


def write_jsonl(records: Iterator[dict[str, object]], output: Path, dataset: str) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    ingested_at = datetime.now(timezone.utc).isoformat()
    count = 0
    with output.open("w", encoding="utf-8") as target:
        for record in records:
            enriched = {**record, "_source_dataset": dataset, "_ingested_at": ingested_at}
            target.write(json.dumps(enriched, sort_keys=True) + "\n")
            count += 1
    return count
