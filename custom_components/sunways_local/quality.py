"""Strict normalization helpers for local inverter values."""

import math
from datetime import datetime
from typing import Any


def valid_value(value: Any) -> Any:
    """Return a HA-safe value without manufacturing false zeroes."""
    if value is None:
        return None
    if isinstance(value, bool | str | datetime):
        return value
    if isinstance(value, int | float):
        return value if math.isfinite(value) else None
    return None


def normalize_runtime(raw: dict[str, Any], supported_ids: set[str]) -> dict[str, Any]:
    """Keep supported fields and discard malformed values."""
    return {key: valid_value(value) for key, value in raw.items() if key in supported_ids}

