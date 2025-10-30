import time
from typing import Dict
from fastapi import HTTPException, status


class RateLimiter:
    """
    Simple in-memory multi-layer rate limiter.

    Layer 1: Per-IP limits
      - 10 requests/minute per IP
      - 1000 requests/day per IP (raised to be lenient during dev)

    Layer 2: API-level limits (placeholder; Twelve Data limits enforced in fetcher)
      - Calls/min to external API handled by fetcher-level limiter

    Layer 3: Cache optimization handled by CacheManager
    """

    def __init__(self) -> None:
        self.per_minute_limit = 10
        self.per_day_limit = 1000
        self._minute_buckets: Dict[str, Dict[str, int]] = {}
        self._day_buckets: Dict[str, Dict[str, int]] = {}
        self.total_requests = 0

    def _now(self) -> int:
        return int(time.time())

    def enforce(self, ip: str) -> None:
        now = self._now()
        minute = now // 60
        day = now // 86400

        # Minute bucket
        minute_bucket = self._minute_buckets.setdefault(ip, {})
        minute_count = minute_bucket.get(str(minute), 0) + 1
        minute_bucket.clear()
        minute_bucket[str(minute)] = minute_count

        if minute_count > self.per_minute_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: 10 requests/min per IP",
            )

        # Day bucket
        day_bucket = self._day_buckets.setdefault(ip, {})
        day_count = day_bucket.get(str(day), 0) + 1
        day_bucket.clear()
        day_bucket[str(day)] = day_count

        if day_count > self.per_day_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Daily limit exceeded",
            )

        self.total_requests += 1

    def get_stats(self) -> Dict:
        return {
            "per_minute_limit": self.per_minute_limit,
            "per_day_limit": self.per_day_limit,
            "total_requests": self.total_requests,
        }


