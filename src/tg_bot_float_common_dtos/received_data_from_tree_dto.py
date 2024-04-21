import dataclasses
import typing

from tg_bot_float_common_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO


@dataclasses.dataclass
class ReceivedDataFromTreeDTO:
    weapons: typing.List[WeaponDTO]
    skins: typing.List[SkinDTO]
    qualities: typing.List[QualityDTO]
    relations: typing.List[RelationDTO]
