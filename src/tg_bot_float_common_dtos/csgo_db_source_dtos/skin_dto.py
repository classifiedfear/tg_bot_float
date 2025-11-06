from typing import Optional

from tg_bot_float_common_dtos.base_dto import BaseDTO


class SkinDTO(BaseDTO):
    name: str
    rarity: Optional[str] = None
