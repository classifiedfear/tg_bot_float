from pydantic import BaseModel


class CsmItemDTO(BaseModel):
    name: str = ""
    item_float: float = 0
    price: float = 0
    price_with_float: float = 0
    overpay_float: float = 0
