from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class Bullet(BaseModel):
    text: str
    sentiment: Sentiment
    evidence: Optional[str] = None

class RichSummary(BaseModel):
    title: str
    bullets: List[Bullet] = Field(min_items=3, max_items=10)
