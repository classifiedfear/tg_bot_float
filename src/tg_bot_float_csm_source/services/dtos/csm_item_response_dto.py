from typing import Any, Dict
from pydantic import BaseModel, ConfigDict


class CsmItemResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fullName: str = ""
    defaultPrice: float = 0
    float: str = ""
    overpay: Dict[str, Any] | None = None
