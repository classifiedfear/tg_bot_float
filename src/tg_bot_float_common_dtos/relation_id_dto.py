from pydantic import BaseModel


class RelationIdDTO(BaseModel):
    weapon_id: int
    skin_id: int
    quality_id: int
