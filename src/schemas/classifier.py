from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Sentiment(str, Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"

class SentimentResult(BaseModel):
    label: Sentiment
    confidence: Optional[float] = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Confidence score between 0 and 1"
    )
    explanation: Optional[str] = Field(
        default=None, max_length=120,
        description="Short reason (<=120 chars)"
    )

