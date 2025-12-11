from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.glove_dto import GloveSkinsDTO


class GlovesPageDTO(BaseDTO):
    gloves: List[GloveSkinsDTO] = []
    count: int
