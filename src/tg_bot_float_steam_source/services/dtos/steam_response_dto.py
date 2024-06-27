from pydantic import BaseModel


class SteamResponseDTO(BaseModel):
    buy_link: str
    inspect_skin_link: str
    price: float
