from typing import List

from pydantic import BaseModel

class CSMWikiSkinDataDTO(BaseModel):
    qualities: List[str] = []
    stattrak_existence: bool = False
