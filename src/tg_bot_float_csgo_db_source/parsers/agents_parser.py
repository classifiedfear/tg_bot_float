from collections import defaultdict
import re
from typing import Generator, List


from tg_bot_float_common_dtos.csgo_db_source_dtos.page_dto import PageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.category_dto import CategoryDTO

from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import SkinDTO
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


class AgentsParser(AbstractParser[PageDTO[SkinDTO]]):
    def __init__(self, settings: ParserSettings) -> None:
        self._agents_regex = re.compile(settings.agent_regex)

    def get_parsed_data(self, page_html: str) -> PageDTO[SkinDTO]:
        agents = self._get_agents(page_html)
        return PageDTO[SkinDTO](items=agents, count=len(agents))

    def _get_agents(self, page_html: str) -> List[CategoryDTO[SkinDTO]]:
        agent_skin_relations: defaultdict[str, List[SkinDTO]] = defaultdict(list)

        for actual_name in self._get_iter_info(self._agents_regex, page_html):
            name, skin, rarity = actual_name.split("|")

            dto = SkinDTO(name=skin, rarity=rarity)
            agent_skin_relations[name].append(dto)

        return [
            CategoryDTO[SkinDTO](category=name, items=skins, count=len(skins))
            for name, skins in agent_skin_relations.items()
        ]

    def _get_iter_info(
        self, pattern: re.Pattern[str], response_text: str
    ) -> Generator[str, None, None]:
        for match in pattern.finditer(response_text):
            yield f"{match.group(1)}|{match.group(2)}|{match.group(3)}"
