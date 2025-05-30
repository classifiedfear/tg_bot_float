from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO


class SkinsDataDTO(BaseDTO):
    name_to_index: dict[str, int]
    skins: List[SkinDTO]
