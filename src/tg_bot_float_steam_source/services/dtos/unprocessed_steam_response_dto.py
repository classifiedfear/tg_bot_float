from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict


class UnprocessedSteamResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    listinginfo: Dict[str, Any] | List[str]
