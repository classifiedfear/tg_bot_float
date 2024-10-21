from typing import List
from pydantic import BaseModel


class SkinsPageDTO(BaseModel):
    weapon_name: str
    skins: List[str]
