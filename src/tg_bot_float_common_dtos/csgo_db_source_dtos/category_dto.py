from typing import Generic, List, TypeVar

from tg_bot_float_common_dtos.base_dto import BaseDTO

T = TypeVar("T")


class CategoryDTO(BaseDTO, Generic[T]):
    category: str
    items: List[T] = []
    count: int
