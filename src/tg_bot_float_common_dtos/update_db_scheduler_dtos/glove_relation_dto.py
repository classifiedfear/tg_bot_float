from typing import List

from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO


class GloveRelationDTO(BaseDTO):
    glove: GloveDTO
    skins: List[SkinDTO]
