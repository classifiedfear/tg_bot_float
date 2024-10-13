from typing import List
from pydantic import BaseModel


class AgentsPageResponseDTO(BaseModel):
    fraction_name: str
    skins: List[str]
