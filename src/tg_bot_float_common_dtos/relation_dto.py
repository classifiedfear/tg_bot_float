import dataclasses

from tg_bot_float_common_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO 

@dataclasses.dataclass
class RelationDTO:
    weapon: WeaponDTO = None
    skin: SkinDTO = None
    quality: QualityDTO = None
