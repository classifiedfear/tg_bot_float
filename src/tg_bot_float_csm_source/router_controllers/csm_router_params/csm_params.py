from pydantic import BaseModel


class CsmParams(BaseModel):
    weapon: str
    skin: str
    quality: str
    stattrak: bool
    offset: int = 0
