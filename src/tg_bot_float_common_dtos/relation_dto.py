from pydantic import BaseModel, ConfigDict

from tg_bot_float_common_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO

class RelationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    weapon: WeaponDTO
    skin: SkinDTO
    quality: QualityDTO
