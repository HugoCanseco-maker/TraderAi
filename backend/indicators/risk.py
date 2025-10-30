import pandas as pd
import numpy as np
from typing import Dict


def calculate_alpha_beta(stock_returns: pd.Series, market_returns: pd.Series, risk_free_rate: float = 0.04) -> Dict:
    aligned = pd.concat([stock_returns, market_returns], axis=1).dropna()
    if len(aligned) < 2:
        return {"alpha": None, "beta": None, "r2": None}
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])[0][1]
    var_m = np.var(aligned.iloc[:, 1])
    if var_m == 0:
        return {"alpha": None, "beta": None, "r2": None}
    beta = cov / var_m
    excess_stock = aligned.iloc[:, 0].mean() * 252 - risk_free_rate
    excess_mkt = aligned.iloc[:, 1].mean() * 252 - risk_free_rate
    alpha = excess_stock - beta * excess_mkt
    r = aligned.iloc[:, 0].corr(aligned.iloc[:, 1])
    return {"alpha": float(alpha), "beta": float(beta), "r2": float(r**2)}


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.04) -> float:
    if returns.std() == 0 or returns.empty:
        return 0.0
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    return float((annual_return - risk_free_rate) / annual_vol)


def calculate_var(returns: pd.Series, confidence: float = 0.95) -> Dict:
    if returns.empty:
        return {"var": None, "cvar": None}
    sorted_ret = returns.sort_values()
    var = float(sorted_ret.quantile(1 - confidence))
    tail = sorted_ret[sorted_ret <= var]
    cvar = float(tail.mean()) if not tail.empty else None
    return {"var": var, "cvar": cvar}


def calculate_max_drawdown(prices: pd.Series) -> Dict:
    roll_max = prices.cummax()
    drawdown = prices / roll_max - 1.0
    max_dd = float(drawdown.min())
    return {"max_drawdown": max_dd}


