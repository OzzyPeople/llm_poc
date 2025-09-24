from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class Trend(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class Forecast(BaseModel):
    month_1: float
    month_2: float
    month_3: float
    trend: Optional[Trend] = None
    reason_why: List[str] = Field(..., min_items=3, max_items=8)
    confidence: float | None = 0.5