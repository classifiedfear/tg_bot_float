from typing import List

from pydantic import BaseModel

from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class SourceDataTreeDTO(BaseModel):
    weapons: List[WeaponDTO]
    skins: List[SkinDTO]
    qualities: List[QualityDTO]
    relations: List[RelationDTO]
