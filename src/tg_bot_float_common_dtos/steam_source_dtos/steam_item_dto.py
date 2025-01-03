from pydantic import BaseModel

class SteamItemDTO(BaseModel):
    name: str
    item_float: float
    price: float
    buy_link: str
