from pydantic import BaseModel


class DeleteUserDataValues(BaseModel):
    tg_user_id: int | None = None
    weapon_id: int | None = None
    skin_id: int | None = None
    quality_id: int | None = None
    stattrak: bool = False
