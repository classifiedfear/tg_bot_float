from typing import Dict, List
from tg_bot_float_common_dtos.schema_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.full_sub_dto import FullSubDTO


class SubsDataDTO(BaseDTO):
    name_to_index: Dict[str, int]
    subs: List[FullSubDTO]
