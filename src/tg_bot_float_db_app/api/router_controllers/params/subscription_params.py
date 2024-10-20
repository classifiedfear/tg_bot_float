from pydantic import BaseModel


class SubscriptionParams(BaseModel):
    telegram_id: int
    weapon_id: int
    skin_id: int
    quality_id: int
    stattrak: bool

