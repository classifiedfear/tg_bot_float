from pydantic import BaseModel, ConfigDict


class WeaponDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = 0
    name: str | None = None
