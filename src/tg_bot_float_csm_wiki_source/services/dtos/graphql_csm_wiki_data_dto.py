from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict


class CsmWikiGraphqlDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    get_min_available: List[Dict[str, Any]] = []
