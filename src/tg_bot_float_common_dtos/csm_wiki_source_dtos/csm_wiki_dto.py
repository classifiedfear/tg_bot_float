from typing import List

from pydantic import BaseModel


class CsmWikiDTO(BaseModel):
    qualities: List[str] = []
    stattrak_existence: bool = False
