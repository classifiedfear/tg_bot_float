from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class WeaponsDataDTO(BaseDTO):
    name_to_index: dict[str, int]
    weapons: List[WeaponDTO]
