import pandas as pd
from typing import Dict

from .confidence import calculate_confidence_score


class ThreeDayPredictor:
    def __init__(self) -> None:
        # Placeholder; models will be wired in later
        pass

    async def predict(self, ticker: str, historical_data: pd.DataFrame) -> Dict:
        # Minimal stub to keep API functional until models are implemented
        current_price = float(historical_data["Close"].iloc[-1]) if not historical_data.empty else None
        score = calculate_confidence_score(0.5, 0.8, 0.5, 0.5, 0.5)
        return {
            "ticker": ticker.upper(),
            "current_price": current_price,
            "predictions": {
                "day_1": {"price": current_price, "change_pct": 0.0},
                "day_2": {"price": current_price, "change_pct": 0.0},
                "day_3": {"price": current_price, "change_pct": 0.0},
            },
            "confidence_score": score["confidence_score"],
            "confidence_level": score["confidence_level"],
            "recommendation": "HOLD",
            "reasoning": {
                "bullish_signals": [],
                "bearish_signals": [],
                "key_indicators": {
                    "momentum": "Neutral",
                    "volatility": "Unknown",
                    "risk": "Unknown",
                    "sentiment": "Neutral",
                },
            },
            "risk_metrics": {
                "sharpe_ratio": None,
                "max_drawdown": None,
                "var_95": None,
                "tail_risk": None,
            },
        }


