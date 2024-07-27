from pydantic import BaseModel


class GetCsmSkinDataParams(BaseModel):
    weapon: str
    skin: str
    quality: str
    stattrak: bool
    offset: int = 0
