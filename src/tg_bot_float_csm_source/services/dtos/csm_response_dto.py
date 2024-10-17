from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict


class CsmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    error: int = 0
    items: List[Dict[str, Any]] = []
