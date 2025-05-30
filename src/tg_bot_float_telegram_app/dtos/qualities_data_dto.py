from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO


class QualitiesDataDTO(BaseDTO):
    name_to_index: dict[str, int]
    qualities: List[QualityDTO]
