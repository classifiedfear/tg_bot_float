from typing import Generic, List, TypeVar
from tg_bot_float_common_dtos.base_dto import BaseDTO


T = TypeVar("T")


class ItemsDataDTO(BaseDTO, Generic[T]):
    name_to_index: dict[str, int]
    items: List[T]
    len_items: int
