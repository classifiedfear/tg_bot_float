from typing import List

from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO


class AgentRelationDTO(BaseDTO):
    agent: AgentDTO
    skins: List[SkinDTO]
