from typing import List
from tg_bot_float_common_dtos.base_dto import BaseDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.agent_dto import AgentSkinsDTO


class AgentsPageDTO(BaseDTO):
    agents: List[AgentSkinsDTO] = []
    count: int
