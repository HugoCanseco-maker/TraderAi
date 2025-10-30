from fastapi import APIRouter, Request, HTTPException
from typing import Dict, List, Any
import time
import pandas as pd

from .rate_limiter import RateLimiter
from ..data.cache_manager import CacheManager
from ..data.fetcher import TwelveDataFetcher
from ..ml.predictor import ThreeDayPredictor
from ..indicators import volatility as vol_mod
from ..indicators import momentum as mom_mod
from ..indicators import risk as risk_mod
from ..indicators import extreme_value as evt_mod
from ..indicators import trend as trend_mod
from ..config import settings


router = APIRouter()

_start_time = time.time()
_cache = CacheManager()
_rate_limiter = RateLimiter()
_fetcher = TwelveDataFetcher(settings.twelve_data_api_key)
_predictor = ThreeDayPredictor()

TOP_30 = [
    "AAPL","MSFT","AMZN","GOOGL","META","NVDA","TSLA","BRK.B","JPM","V",
    "UNH","HD","MA","PG","XOM","AVGO","LLY","JNJ","WMT","CVX",
    "KO","PFE","BAC","DIS","PEP","ABBV","COST","CSCO","ADBE","NFLX"
]


def _to_dataframe(values: List[Dict[str, Any]]) -> pd.DataFrame:
    if not values:
        return pd.DataFrame()
    df = pd.DataFrame(values)
    # Normalize column names
    mapping = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date",
    }
    for k, v in mapping.items():
        if k in df.columns:
            df[v] = pd.to_numeric(df[k], errors="coerce") if k != "datetime" else pd.to_datetime(df[k])
    if "Date" in df.columns:
        df = df.sort_values("Date").reset_index(drop=True)
        df.set_index("Date", inplace=True)
    return df[[c for c in ["Open","High","Low","Close","Volume"] if c in df.columns]]


@router.get("/health")
async def health() -> Dict:
    uptime_seconds = int(time.time() - _start_time)
    return {
        "status": "healthy",
        "uptime": uptime_seconds,
        "cache_stats": _cache.get_stats(),
        "rate_limiter": _rate_limiter.get_stats(),
    }


@router.get("/predict/{ticker}")
async def predict_ticker(ticker: str, request: Request) -> Dict:
    client_ip = request.client.host if request.client else "unknown"
    _rate_limiter.enforce(client_ip)
    tkr = ticker.upper()
    cached = _cache.get(f"predict:{tkr}")
    if cached:
        return cached
    try:
        ts = _fetcher.get_time_series(tkr, interval="1day", outputsize=120)
        df = _to_dataframe(ts)
        if df.empty:
            raise HTTPException(status_code=404, detail="No data")
        result = await _predictor.predict(tkr, df)
        _cache.set(f"predict:{tkr}", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/{ticker}")
async def stock_analysis(ticker: str, request: Request) -> Dict:
    client_ip = request.client.host if request.client else "unknown"
    _rate_limiter.enforce(client_ip)
    tkr = ticker.upper()
    cached = _cache.get(f"stock:{tkr}")
    if cached:
        return cached
    ts = _fetcher.get_time_series(tkr, interval="1day", outputsize=200)
    df = _to_dataframe(ts)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data")

    # Indicators
    atr = vol_mod.calculate_atr(df)
    bb = vol_mod.calculate_bollinger_bands(df["Close"]) if "Close" in df else {}
    hv = vol_mod.calculate_historical_volatility(df["Close"].pct_change().dropna()) if "Close" in df else None
    macdv = mom_mod.calculate_macd_v(df)
    rsi = mom_mod.calculate_rsi(df["Close"]) if "Close" in df else {"rsi": None}
    stoch = mom_mod.calculate_stochastic(df)
    mdd = risk_mod.calculate_max_drawdown(df["Close"]) if "Close" in df else {"max_drawdown": None}
    var = risk_mod.calculate_var(df["Close"].pct_change().dropna()) if "Close" in df else {"var": None, "cvar": None}
    tail = evt_mod.calculate_tail_risk(df["Close"].pct_change().dropna()) if "Close" in df else {}

    payload = {
        "ticker": tkr,
        "current_price": float(df["Close"].iloc[-1]) if "Close" in df and not df.empty else None,
        "volatility": {
            "atr": float(atr.iloc[-1]) if len(atr) else None,
            "bollinger": {k: (float(v.iloc[-1]) if hasattr(v, "iloc") else None) for k, v in bb.items()} if bb else {},
            "historical_volatility": hv,
        },
        "momentum": {
            "macd_v": float(macdv["macd_v"].iloc[-1]) if len(macdv["macd_v"]) else None,
            "signal": float(macdv["signal"].iloc[-1]) if len(macdv["signal"]) else None,
            "hist": float(macdv["hist"].iloc[-1]) if len(macdv["hist"]) else None,
            "rsi": float(rsi.get("rsi").iloc[-1]) if rsi.get("rsi") is not None else None,
            "stochastic": {
                "k": float(stoch["%K"].iloc[-1]) if len(stoch["%K"]) else None,
                "d": float(stoch["%D"].iloc[-1]) if len(stoch["%D"]) else None,
            },
        },
        "risk": {
            "max_drawdown": mdd.get("max_drawdown"),
            "var": var.get("var"),
            "cvar": var.get("cvar"),
            "tail_risk": tail,
        },
    }
    _cache.set(f"stock:{tkr}", payload)
    return payload


@router.get("/watchlist")
async def get_watchlist(request: Request) -> Dict:
    client_ip = request.client.host if request.client else "unknown"
    _rate_limiter.enforce(client_ip)
    cached = _cache.get("watchlist")
    if cached:
        return cached
    items = []
    for t in TOP_30:
        try:
            ts = _fetcher.get_time_series(t, outputsize=2)
            df = _to_dataframe(ts)
            if not df.empty:
                last = float(df["Close"].iloc[-1])
                prev = float(df["Close"].iloc[-2]) if len(df) > 1 else last
                change_pct = ((last - prev) / prev) * 100 if prev else 0.0
                items.append({"ticker": t, "price": last, "change_pct": round(change_pct, 2)})
        except Exception:
            continue
    payload = {"watchlist": items}
    _cache.set("watchlist", payload)
    return payload


@router.post("/watchlist/refresh")
async def refresh_watchlist(request: Request) -> Dict:
    client_ip = request.client.host if request.client else "unknown"
    _rate_limiter.enforce(client_ip)
    # Invalidate and rebuild
    _cache.set("watchlist", None)
    return await get_watchlist(request)


@router.get("/trending")
async def trending(limit: int = 10, request: Request = None) -> Dict:
    if request and request.client:
        _rate_limiter.enforce(request.client.host)
    items = []
    for t in TOP_30:
        try:
            ts = _fetcher.get_time_series(t, outputsize=6)
            df = _to_dataframe(ts)
            if not df.empty:
                last = float(df["Close"].iloc[-1])
                prev5 = float(df["Close"].iloc[-5]) if len(df) > 5 else float(df["Close"].iloc[0])
                change_pct = ((last - prev5) / prev5) * 100 if prev5 else 0.0
                vol = float(df["Volume"].iloc[-1]) if "Volume" in df else None
                items.append({"ticker": t, "change_5d_pct": round(change_pct, 2), "volume": vol})
        except Exception:
            continue
    items.sort(key=lambda x: x.get("change_5d_pct", 0), reverse=True)
    return {"trending": items[: max(1, min(limit, 50))]}


@router.get("/indicators/{ticker}")
async def indicators(ticker: str, request: Request, indicators: str = "all") -> Dict:
    client_ip = request.client.host if request.client else "unknown"
    _rate_limiter.enforce(client_ip)
    tkr = ticker.upper()
    ts = _fetcher.get_time_series(tkr, outputsize=200)
    df = _to_dataframe(ts)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data")
    payload = {
        "ticker": tkr,
        "close": df["Close"].dropna().tail(120).tolist() if "Close" in df else [],
        "atr": vol_mod.calculate_atr(df).dropna().tail(120).tolist(),
        "bollinger": {
            "upper": vol_mod.calculate_bollinger_bands(df["Close"]).get("upper").dropna().tail(120).tolist(),
            "middle": vol_mod.calculate_bollinger_bands(df["Close"]).get("middle").dropna().tail(120).tolist(),
            "lower": vol_mod.calculate_bollinger_bands(df["Close"]).get("lower").dropna().tail(120).tolist(),
        },
        "rsi": mom_mod.calculate_rsi(df["Close"]).get("rsi").dropna().tail(120).tolist(),
        "stochastic": {
            "k": mom_mod.calculate_stochastic(df).get("%K").dropna().tail(120).tolist(),
            "d": mom_mod.calculate_stochastic(df).get("%D").dropna().tail(120).tolist(),
        },
        "ema": {
            "ema20": trend_mod.ema(df["Close"], 20).dropna().tail(120).tolist(),
            "ema50": trend_mod.ema(df["Close"], 50).dropna().tail(120).tolist(),
            "ema200": trend_mod.ema(df["Close"], 200).dropna().tail(120).tolist(),
        },
        "sma": {
            "sma20": trend_mod.sma(df["Close"], 20).dropna().tail(120).tolist(),
            "sma50": trend_mod.sma(df["Close"], 50).dropna().tail(120).tolist(),
            "sma200": trend_mod.sma(df["Close"], 200).dropna().tail(120).tolist(),
        },
    }
    return payload


@router.get("/performance")
async def performance() -> Dict:
    # Placeholder performance stats to be replaced with tracked metrics
    return {
        "strategy_accuracy_3d": 0.6,
        "baseline_accuracy": 0.5,
        "avg_confidence": 0.65,
    }


@router.get("/stats")
async def stats() -> Dict:
    return {
        "rate_limiter": _rate_limiter.get_stats(),
        "cache": _cache.get_stats(),
        "uptime": int(time.time() - _start_time),
    }


