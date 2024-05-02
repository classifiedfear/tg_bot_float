from pydantic import BaseModel



class SkinDTO(BaseModel):
    id: int = 0
    name: str | None = None
    stattrak_existence: bool = False
