from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


_analyzer = SentimentIntensityAnalyzer()


def score_text(text: str) -> float:
    scores = _analyzer.polarity_scores(text or "")
    return float(scores.get("compound", 0.0))


