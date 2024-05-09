from pydantic import BaseModel, ConfigDict


class RelationIdDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    weapon_id: int
    skin_id: int
    quality_id: int
