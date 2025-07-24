from functools import lru_cache
from typing import Literal
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

@lru_cache
def _vader() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()

def get_sentiment(text: str) -> Literal["POSITIVE", "NEGATIVE", "NEUTRAL"]:
    c = _vader().polarity_scores(text)["compound"]
    if c >=  0.05: return "POSITIVE"
    if c <= -0.05: return "NEGATIVE"
    return "NEUTRAL"

# --- HuggingFace alternative (commented) ---------------
# from transformers import pipeline
# _hf = pipeline("sentiment-analysis",
#                model="distilbert-base-uncased-finetuned-sst-2-english",
#                device_map="auto")
# def get_sentiment(text: str) -> Literal["POSITIVE", "NEGATIVE", "NEUTRAL"]:
#     lbl = _hf(text, max_length=256)[0]["label"]
#     return "POSITIVE" if lbl == "POSITIVE" else "NEGATIVE"
