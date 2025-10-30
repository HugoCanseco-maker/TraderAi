import os
from typing import Dict, List
import time
import requests


class RateLimiter:
    def __init__(self, calls_per_minute: int = 8) -> None:
        self.calls_per_minute = calls_per_minute
        self._timestamps: List[float] = []

    def acquire(self) -> None:
        now = time.time()
        # Prune timestamps older than 60 seconds
        self._timestamps = [t for t in self._timestamps if now - t < 60]
        if len(self._timestamps) >= self.calls_per_minute:
            sleep_time = 60 - (now - self._timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self._timestamps.append(time.time())


class TwelveDataFetcher:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("TWELVE_DATA_API_KEY", "")
        self.rate_limiter = RateLimiter(calls_per_minute=8)
        self.base_url = "https://api.twelvedata.com"

    def _get(self, path: str, params: Dict) -> Dict:
        self.rate_limiter.acquire()
        params = {"apikey": self.api_key, **params}
        url = f"{self.base_url}/{path}"
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Twelve Data returns {"code":..., "message":...} on error
        if isinstance(data, dict) and data.get("code"):
            raise RuntimeError(data.get("message", "Twelve Data API error"))
        return data

    def get_quote(self, ticker: str) -> Dict:
        return self._get("quote", {"symbol": ticker})

    def get_time_series(self, ticker: str, interval: str = "1day", outputsize: int = 90) -> List[Dict]:
        data = self._get("time_series", {"symbol": ticker, "interval": interval, "outputsize": outputsize})
        return data.get("values", []) if isinstance(data, dict) else data

    def get_fundamentals(self, ticker: str) -> Dict:
        return self._get("fundamentals", {"symbol": ticker})

    def get_technical_indicator(self, ticker: str, indicator: str, params: Dict) -> Dict:
        query = {"symbol": ticker, **params}
        return self._get(indicator, query)


