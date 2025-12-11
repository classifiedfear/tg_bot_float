from typing import Dict, Generator, List
import re


from tg_bot_float_common_dtos.csgo_db_source_dtos.glove_dto import GloveSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings

from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser


class GlovesParser(AbstractParser[GlovesPageDTO]):
    def __init__(self, settings: ParserSettings) -> None:
        self._glove_regex = re.compile(settings.glove_regex)

    def get_parsed_data(self, page_html: str) -> GlovesPageDTO:
        if page_html == "":
            raise CsgoDbException("No gloves found!")

        gloves = self._get_gloves(page_html)
        return GlovesPageDTO(gloves=gloves, count=sum(map(lambda dto: len(dto.skins), gloves)))

    def _get_gloves(self, page_html: str) -> List[GloveSkinsDTO]:
        glove_skin_relations: Dict[str, GloveSkinsDTO] = {}

        for actual_name in self._get_iter_info(self._glove_regex, page_html):

            name, skin = actual_name.split("|")

            if dto := glove_skin_relations.get(name):
                dto.skins.append(skin)
                dto.count += 1
            else:
                glove_skin_relations[name] = GloveSkinsDTO(glove_name=name, skins=[skin], count=1)

        if len(glove_skin_relations) == 0:
            raise CsgoDbException("Wrong page request!")

        return list(glove_skin_relations.values())

    def _get_iter_info(
        self, pattern: re.Pattern[str], response_text: str
    ) -> Generator[str, None, None]:
        for match in pattern.finditer(response_text):
            first_group, second_group = match.group(1), match.group(2)
            yield f"{first_group}|{second_group}"
