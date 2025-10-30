import pandas as pd
from typing import Dict


def calculate_atr(prices: pd.DataFrame, period: int = 14) -> pd.Series:
    high = prices["High"]
    low = prices["Low"]
    close = prices["Close"].shift(1)
    tr = pd.concat([(high - low).abs(), (high - close).abs(), (low - close).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / period, adjust=False).mean()
    return atr


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Dict:
    mid = prices.rolling(window=period).mean()
    sd = prices.rolling(window=period).std()
    upper = mid + std_dev * sd
    lower = mid - std_dev * sd
    bandwidth = (upper - lower) / mid
    pb = (prices - lower) / (upper - lower)
    return {"upper": upper, "middle": mid, "lower": lower, "bandwidth": bandwidth, "%b": pb}


def calculate_historical_volatility(returns: pd.Series, window: int = 20) -> float:
    return float((returns.rolling(window=window).std() * (252 ** 0.5)).iloc[-1])


