from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict


class GraphqlResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    errors: List[Dict[str, Any]] = []
    data: Dict[str, Any] = {}
