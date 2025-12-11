from typing import List

from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import CategoryWeaponsDTO


class WeaponsPageDTO(BaseDTO):
    categories: List[CategoryWeaponsDTO] = []
    count: int
