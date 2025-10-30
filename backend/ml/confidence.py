from typing import Dict


def calculate_confidence_score(
    model_agreement: float,
    data_quality: float,
    volatility_score: float,
    sentiment_consistency: float,
    technical_alignment: float,
) -> Dict:
    weights = {
        "model_agreement": 0.35,
        "data_quality": 0.15,
        "volatility": 0.20,
        "sentiment": 0.15,
        "technical": 0.15,
    }
    score = (
        model_agreement * weights["model_agreement"]
        + data_quality * weights["data_quality"]
        + volatility_score * weights["volatility"]
        + sentiment_consistency * weights["sentiment"]
        + technical_alignment * weights["technical"]
    )
    level = "Low"
    if score > 0.7:
        level = "High"
    elif score >= 0.5:
        level = "Medium"
    return {
        "confidence_score": round(score, 2),
        "confidence_level": level,
        "factors": {
            "model_agreement": model_agreement,
            "data_quality": data_quality,
            "volatility": volatility_score,
            "sentiment": sentiment_consistency,
            "technical": technical_alignment,
        },
    }


