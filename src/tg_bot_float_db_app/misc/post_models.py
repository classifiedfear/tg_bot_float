from pydantic import BaseModel


class SkinPostModel(BaseModel):
    name: str
    stattrak_existence: bool = False


class QualityPostModel(BaseModel):
    name: str


class WeaponPostModel(BaseModel):
    name: str


class RelationPostModel(BaseModel):
    weapon_id: int
    skin_id: int
    quality_id: int