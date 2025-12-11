from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO


class AgentSkinsDTO(BaseDTO):
    fraction_name: str
    skins: List[str] = []
    count: int
