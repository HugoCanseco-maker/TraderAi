from pydantic import BaseModel
from typing import Dict, Optional


class DayPrediction(BaseModel):
    price: Optional[float] = None
    change_pct: Optional[float] = None


class PredictionResponse(BaseModel):
    ticker: str
    current_price: Optional[float] = None
    predictions: Dict[str, DayPrediction]
    confidence_score: float
    confidence_level: str
    recommendation: str
    reasoning: Dict
    risk_metrics: Dict


