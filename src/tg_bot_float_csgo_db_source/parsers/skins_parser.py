from typing import Generator, List
import re
from itertools import islice
from collections import Counter

from tg_bot_float_common_dtos.csgo_db_source_dtos.page_dto import PageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.category_dto import CategoryDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


class SkinsParser(AbstractParser[PageDTO[SkinDTO]]):
    def __init__(self, settings: ParserSettings) -> None:
        self._skin_name_regex = re.compile(settings.skin_name_regex)
        self._skin_weapon_name_regex = re.compile(settings.skin_weapon_name_regex)
        self._skin_rarity_regex = re.compile(settings.skin_rarity_regex)

    def _get_correct_weapon_name(self, page_html: str) -> str:
        if weapon_name := self._extract_regex(self._skin_weapon_name_regex, page_html):
            return weapon_name
        raise CsgoDbException("Weapon not found in HTML")

    def get_parsed_data(self, page_html: str) -> PageDTO[SkinDTO]:
        category_dtos: List[CategoryDTO[SkinDTO]] = []

        dtos_gen = self._get_skin_dtos(page_html)

        rarity_counter: Counter[str] = self._count_rarity(page_html)

        correct_weapon_name = self._get_correct_weapon_name(page_html)

        for rarity, count in rarity_counter.items():
            actual_count = count
            actual_rarity = rarity
            dtos_chunk = list(islice(dtos_gen, count))

            for dto in dtos_chunk:
                dto.rarity = actual_rarity

            if dtos_chunk and dtos_chunk[0].name == "Vanilla":
                dtos_chunk.pop(0)
                actual_count -= 1

            dto = CategoryDTO[SkinDTO](
                category=correct_weapon_name,
                items=dtos_chunk,
                count=actual_count,
            )
            category_dtos.append(dto)

        return PageDTO[SkinDTO](
            items=category_dtos,
            count=sum(map(lambda dto: dto.count, category_dtos)),
        )

    def _get_skin_dtos(self, page_html: str) -> Generator[SkinDTO, None, None]:
        for name in self._get_iter_info(self._skin_name_regex, page_html):
            yield SkinDTO(name=name)

    def _count_rarity(self, response_text: str) -> Counter[str]:
        return Counter(match.group(1) for match in self._skin_rarity_regex.finditer(response_text))
