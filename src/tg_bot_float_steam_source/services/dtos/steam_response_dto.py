from typing import Any, Dict
from pydantic import BaseModel, ConfigDict


class SteamResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    listinginfo: Dict[str, Any]
