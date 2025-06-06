from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class RelationDataDTO(BaseDTO):
    weapon: WeaponDTO
    skin: SkinDTO
    quality: QualityDTO
    stattrak_existence: bool
