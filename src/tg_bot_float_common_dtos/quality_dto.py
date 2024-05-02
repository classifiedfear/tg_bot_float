from pydantic import BaseModel

class QualityDTO(BaseModel):
    id: int = 0
    name: str | None = None
