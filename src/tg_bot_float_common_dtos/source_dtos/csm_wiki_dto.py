from typing import List
from pydantic import BaseModel, ConfigDict


class CsmWikiDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    qualities: List[str] = []
    stattrak_existence: bool = False
