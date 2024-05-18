from pydantic import BaseModel

class SteamItemResponseDTO(BaseModel):
    name: str
    item_float: float
    price: float
    buy_link: str
