from collections import defaultdict
import re
from typing import Dict, List

from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import (
    AgentsPageDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class AgentsPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._agent_regex = re.compile(self._settings.agent_regex_pattern)

    async def get_agent_names(self) -> List[AgentsPageDTO]:
        agents: Dict[str, List[str]] = defaultdict(list)
        response_text = await self._get_response(
            self._settings.base_url + self._settings.agents_page
        )
        for match in self._agent_regex.finditer(response_text):
            agents[match.group(1)].append(match.group(2))

        return [
            AgentsPageDTO(fraction_name=fraction, skins=skins)
            for fraction, skins in agents.items()
        ]
