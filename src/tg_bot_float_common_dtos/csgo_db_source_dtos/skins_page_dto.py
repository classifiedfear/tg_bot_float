from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import WeaponSkinsDTO


class SkinsPageDTO(BaseDTO):
    weapon_name: str
    skins: List[WeaponSkinsDTO] = []
    count: int
