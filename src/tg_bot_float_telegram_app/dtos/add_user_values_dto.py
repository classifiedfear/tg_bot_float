from pydantic import BaseModel


class AddUserDataValues(BaseModel):
    tg_user_id: int | None = None
    weapon_id: int | None = None
    weapon_name: str | None = None
    skin_id: int | None = None
    skin_name: str | None = None
    quality_id: int | None = None
    quality_name: str | None = None
    stattrak: bool = False
