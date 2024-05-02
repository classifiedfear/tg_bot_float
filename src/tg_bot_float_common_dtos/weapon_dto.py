from pydantic import BaseModel


class WeaponDTO(BaseModel):
    id: int = 0
    name: str | None = None
