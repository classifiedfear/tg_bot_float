from pydantic import BaseModel


class CsmItemResponseDTO(BaseModel):
    name: str
    item_float: float
    price: float
    price_with_float: float
    overpay_float: float
