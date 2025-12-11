import re
from typing import Dict, Generator, List


from tg_bot_float_common_dtos.csgo_db_source_dtos.agent_dto import AgentSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


class AgentsParser(AbstractParser[AgentsPageDTO]):
    def __init__(self, settings: ParserSettings) -> None:
        self._agents_regex = re.compile(settings.agent_regex)

    def get_parsed_data(self, page_html: str) -> AgentsPageDTO:
        if page_html == "":
            raise CsgoDbException("No agents found!")

        agents = self._get_agents(page_html)
        return AgentsPageDTO(agents=agents, count=sum(map(lambda dto: len(dto.skins), agents)))

    def _get_agents(self, page_html: str) -> List[AgentSkinsDTO]:
        agent_skin_relations: Dict[str, AgentSkinsDTO] = {}

        for actual_name in self._get_iter_info(self._agents_regex, page_html):
            name, skin = actual_name.split("|")

            if dto := agent_skin_relations.get(name):
                dto.skins.append(skin)
                dto.count += 1
            else:
                agent_skin_relations[name] = AgentSkinsDTO(
                    fraction_name=name, skins=[skin], count=1
                )

        if len(agent_skin_relations) == 0:
            raise CsgoDbException("Wrong page request!")

        return list(agent_skin_relations.values())

    def _get_iter_info(
        self, pattern: re.Pattern[str], response_text: str
    ) -> Generator[str, None, None]:
        for match in pattern.finditer(response_text):
            yield f"{match.group(1)}|{match.group(2)}"
