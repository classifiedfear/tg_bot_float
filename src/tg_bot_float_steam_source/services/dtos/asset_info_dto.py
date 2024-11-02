from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict


class AssetInfoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appid: int
    contextid: str
    id: str
    market_actions: List[Dict[str, Any]]
