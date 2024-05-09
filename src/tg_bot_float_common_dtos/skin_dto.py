from pydantic import BaseModel, ConfigDict



class SkinDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = 0
    name: str | None = None
    stattrak_existence: bool | None = None
