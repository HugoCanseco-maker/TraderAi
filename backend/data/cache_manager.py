import json
import os
import time
from datetime import timedelta
from typing import Dict, Optional, Any


class CacheManager:
    """
    Smart caching system with TTL and validation.

    - Default 30-minute TTL
    - Persistent storage (JSON)
    - Cache hit/miss tracking
    """

    def __init__(self, cache_file: str = "stock_cache.json", ttl_minutes: int = 30) -> None:
        self.cache_file = os.path.join(os.path.dirname(__file__), cache_file)
        self.ttl = timedelta(minutes=ttl_minutes)
        self.cache: Dict[str, Any] = self._load_cache()
        self.hits = 0
        self.misses = 0

    def _load_cache(self) -> Dict[str, Any]:
        if not os.path.exists(self.cache_file):
            return {}
        try:
            with open(self.cache_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f)
        except Exception:
            # Fail silently for now; logging will be added later
            pass

    def _now(self) -> int:
        return int(time.time())

    def get(self, ticker: str) -> Optional[Dict]:
        ticker = ticker.upper()
        if not self.is_valid(ticker):
            self.misses += 1
            return None
        self.hits += 1
        return self.cache.get(ticker, {}).get("data")

    def set(self, ticker: str, data: Dict) -> None:
        ticker = ticker.upper()
        self.cache[ticker] = {"data": data, "timestamp": self._now()}
        self._save_cache()

    def is_valid(self, ticker: str) -> bool:
        ticker = ticker.upper()
        entry = self.cache.get(ticker)
        if not entry or "timestamp" not in entry:
            return False
        age_seconds = self._now() - int(entry["timestamp"])
        return age_seconds < int(self.ttl.total_seconds())

    def get_stats(self) -> Dict:
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache)}


