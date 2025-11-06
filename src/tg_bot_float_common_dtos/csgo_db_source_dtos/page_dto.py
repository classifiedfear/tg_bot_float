from typing import Generic, List, TypeVar

from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.category_dto import CategoryDTO


T = TypeVar("T")


class PageDTO(BaseDTO, Generic[T]):
    items: List[CategoryDTO[T]]
    count: int
