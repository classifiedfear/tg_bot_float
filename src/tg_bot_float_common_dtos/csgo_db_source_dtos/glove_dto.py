from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO


class GloveSkinsDTO(BaseDTO):
    glove_name: str
    skins: List[str] = []
    count: int
