"""Source-aligned quality rules for collision records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class QualityResult:
    valid: bool
    reasons: tuple[str, ...]


def _number(value: Any, default: float = 0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def validate_crash(record: Mapping[str, Any]) -> QualityResult:
    reasons: list[str] = []
    if not record.get("collision_id"):
        reasons.append("missing_collision_id")

    try:
        datetime.fromisoformat(str(record.get("crash_date", "")).replace("Z", "+00:00"))
    except ValueError:
        reasons.append("invalid_crash_date")

    for field in ("number_of_persons_injured", "number_of_persons_killed"):
        try:
            if _number(record.get(field)) < 0:
                reasons.append(f"negative_{field}")
        except (TypeError, ValueError):
            reasons.append(f"invalid_{field}")

    try:
        latitude = _number(record.get("latitude"), default=0)
        longitude = _number(record.get("longitude"), default=0)
        if latitude and not -90 <= latitude <= 90:
            reasons.append("invalid_latitude")
        if longitude and not -180 <= longitude <= 180:
            reasons.append("invalid_longitude")
    except (TypeError, ValueError):
        reasons.append("invalid_coordinates")

    try:
        total_injured = _number(record.get("number_of_persons_injured"))
        component_injured = sum(
            _number(record.get(field))
            for field in (
                "number_of_pedestrians_injured",
                "number_of_cyclist_injured",
                "number_of_motorist_injured",
            )
        )
        if component_injured > total_injured:
            reasons.append("injury_components_exceed_total")
    except (TypeError, ValueError):
        reasons.append("invalid_injury_component")

    return QualityResult(not reasons, tuple(reasons))
