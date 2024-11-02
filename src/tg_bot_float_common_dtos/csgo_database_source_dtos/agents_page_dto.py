from typing import List
from pydantic import BaseModel


class AgentsPageDTO(BaseModel):
    fraction_name: str
    skins: List[str]
