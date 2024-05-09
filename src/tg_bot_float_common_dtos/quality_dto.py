from pydantic import BaseModel, ConfigDict


class QualityDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = 0
    name: str | None = None
