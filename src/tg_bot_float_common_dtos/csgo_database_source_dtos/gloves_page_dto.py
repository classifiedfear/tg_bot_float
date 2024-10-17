from typing import List
from pydantic import BaseModel


class GlovesPageDTO(BaseModel):
    glove_name: str
    skins: List[str]
