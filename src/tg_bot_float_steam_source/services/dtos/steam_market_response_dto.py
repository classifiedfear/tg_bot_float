from pydantic import BaseModel


class SteamMarketResponseDTO(BaseModel):
    buy_link: str
    inspect_skin_link: str
    price: float
