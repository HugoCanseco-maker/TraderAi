import pandas as pd


def vwap(df: pd.DataFrame) -> pd.Series:
    pv = df["Close"] * df["Volume"].fillna(0)
    cum_pv = pv.cumsum()
    cum_vol = df["Volume"].fillna(0).cumsum().replace(0, pd.NA)
    return cum_pv / cum_vol


def obv(df: pd.DataFrame) -> pd.Series:
    direction = df["Close"].diff().fillna(0).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    vol = df["Volume"].fillna(0)
    return (direction * vol).cumsum()


def volume_roc(df: pd.DataFrame, period: int = 10) -> pd.Series:
    v = df["Volume"].fillna(0)
    return v.pct_change(periods=period)


