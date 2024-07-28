from pydantic import BaseModel


class DataFromSteam(BaseModel):
    buy_link: str
    inspect_skin_link: str
    price: float
