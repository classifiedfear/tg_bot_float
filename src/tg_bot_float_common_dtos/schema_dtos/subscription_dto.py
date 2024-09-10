from pydantic import BaseModel


class SubscriptionDTO(BaseModel):
    weapon_id: int
    weapon_name: str
    skin_id: int
    skin_name: str
    quality_id: int
    quality_name: str
    stattrak: bool
