from typing import List
from pydantic import BaseModel


class GlovesPageResponseDTO(BaseModel):
    glove_name: str
    skins: List[str]
