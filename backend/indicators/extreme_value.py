import pandas as pd
from typing import Dict


def calculate_tail_risk(returns: pd.Series, threshold_percentile: float = 0.95) -> Dict:
    if returns.empty:
        return {"tail_risk_prob": None, "expected_extreme_loss": None, "worst_99": None, "kurtosis": None}
    thr = returns.quantile(1 - threshold_percentile)
    tail = returns[returns <= thr]
    prob = float(len(tail) / len(returns)) if len(returns) else 0.0
    expected_loss = float(tail.mean()) if not tail.empty else None
    worst_99 = float(returns.quantile(0.01))
    return {"tail_risk_prob": prob, "expected_extreme_loss": expected_loss, "worst_99": worst_99, "kurtosis": float(returns.kurt())}


def calculate_return_distribution(returns: pd.Series) -> Dict:
    if returns.empty:
        return {"skew": None, "kurtosis": None}
    return {"skew": float(returns.skew()), "kurtosis": float(returns.kurt())}


