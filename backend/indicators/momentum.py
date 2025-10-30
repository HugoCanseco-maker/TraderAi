import pandas as pd
from typing import Dict


def calculate_macd_v(prices: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    pv = prices["Close"] * prices["Volume"].fillna(0)
    ema_fast = pv.ewm(span=fast, adjust=False).mean()
    ema_slow = pv.ewm(span=slow, adjust=False).mean()
    macd_v = ema_fast - ema_slow
    signal_line = macd_v.ewm(span=signal, adjust=False).mean()
    hist = macd_v - signal_line
    return {"macd_v": macd_v, "signal": signal_line, "hist": hist}


def calculate_rsi(prices: pd.Series, period: int = 14) -> Dict:
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    return {"rsi": rsi}


def calculate_stochastic(prices: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Dict:
    low_min = prices["Low"].rolling(window=k_period).min()
    high_max = prices["High"].rolling(window=k_period).max()
    k = ((prices["Close"] - low_min) / (high_max - low_min)) * 100
    d = k.rolling(window=d_period).mean()
    return {"%K": k, "%D": d}


