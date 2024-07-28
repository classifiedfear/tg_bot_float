from pydantic import BaseModel


class GetSteamSkinDataParams(BaseModel):
    weapon: str
    skin: str
    quality: str
    stattrak: bool
    start: int = 0
    count: int = 10
    currency: int = 1
