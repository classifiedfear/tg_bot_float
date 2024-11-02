from typing import Dict, Any

from pydantic import BaseModel, ConfigDict


class CsFloatResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    iteminfo: Dict[str, Any] = {}
