from typing import Any


def safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


