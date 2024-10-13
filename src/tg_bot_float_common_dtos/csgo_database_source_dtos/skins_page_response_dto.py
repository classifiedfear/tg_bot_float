from typing import List
from pydantic import BaseModel


class SkinsPageResponseDTO(BaseModel):
    weapon_name: str
    skins: List[str]
