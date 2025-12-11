from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO


class CategoryWeaponsDTO(BaseDTO):
    category: str
    weapons: List[str] = []
    count: int
