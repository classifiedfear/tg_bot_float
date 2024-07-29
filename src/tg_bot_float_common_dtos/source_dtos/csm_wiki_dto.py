from typing import List

from pydantic import BaseModel


class CSMWikiDTO(BaseModel):
    qualities: List[str] = []
    stattrak_existence: bool = False
