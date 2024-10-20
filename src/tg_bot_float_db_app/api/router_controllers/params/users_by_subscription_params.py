from pydantic import BaseModel


class UsersBySubscriptionParams(BaseModel):
    weapon_id: int
    skin_id: int
    quality_id: int
    stattrak: bool
