from typing import Literal, Optional, Union, Dict, Any, List
from pydantic import BaseModel, Field

EntityType = Literal[
    "date","amount","phone","email","url","iban","vat","zipcode","currency","country","name","address"
]

class NormalizedEntity(BaseModel):
    #model_config = {"extra": "forbid"}
    type: EntityType
    raw: str
    # normalized can be a scalar or structured object (e.g., address parts)
    normalized: Optional[Union[str, float, Dict[str, Any]]] = None
    confidence: float = Field(ge=0.0, le=1.0)

class NormalizeResult(BaseModel):
    #model_config = {"extra": "forbid"}
    entities: List[NormalizedEntity]
    unparsed: List[str] = []

