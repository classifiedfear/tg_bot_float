from typing import List

from pydantic import BaseModel


class WeaponsPageDTO(BaseModel):
    weapons: List[str]
    knives: List[str]
    other: List[str]
