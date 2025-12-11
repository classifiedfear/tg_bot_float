from typing import List

from tg_bot_float_common_dtos.base_dto import BaseDTO


class QualityStattrakDTO(BaseDTO):
    qualities: List[str] = []
    stattrak_qualities: List[str] = []
    stattrak_existence: bool = False
