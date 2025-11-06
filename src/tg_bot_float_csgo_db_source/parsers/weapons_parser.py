from typing import Generator, List
import re
from itertools import islice

from tg_bot_float_common_dtos.csgo_db_source_dtos.page_dto import PageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.category_dto import CategoryDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import WeaponDTO
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser


class WeaponsParser(AbstractParser[PageDTO[WeaponDTO]]):
    def __init__(self, settings: ParserSettings) -> None:
        self._total_weapon_regex = re.compile(settings.total_weapon_regex)
        self._weapon_name_regex = re.compile(settings.weapon_name_regex)
        self._weapon_category_number_regex = re.compile(settings.weapon_category_number_regex)
        self._tags_regex = re.compile(r"<[^>]+>")

    def get_parsed_data(self, page_html: str) -> PageDTO[WeaponDTO]:
        item_dtos: List[CategoryDTO[WeaponDTO]] = []

        dtos_gen = self._get_weapon_dtos(page_html)

        for dto in self._get_weapon_dtos_without_names(page_html):
            dtos_chunk = list(islice(dtos_gen, dto.count))
            dto.items = dtos_chunk

            if dto.category == "heavy weapons":
                dto.category = "heavy"

            item_dtos.append(dto)

        remaining = list(dtos_gen)

        if remaining:
            item_dtos.append(
                CategoryDTO[WeaponDTO](category="other", items=remaining, count=len(remaining))
            )

        return PageDTO[WeaponDTO](items=item_dtos, count=sum(map(lambda dto: dto.count, item_dtos)))

    def _get_weapon_dtos(self, page_html: str):
        for name in self._get_iter_info(self._weapon_name_regex, page_html):
            yield WeaponDTO(name=name)

    def _get_weapon_dtos_without_names(
        self, response_text: str
    ) -> Generator[CategoryDTO[WeaponDTO], None, None]:
        total_weapon_text = self._total_weapon_regex.search(response_text)

        if total_weapon_text:

            text_without_tags = self._tags_regex.sub("", total_weapon_text.group(0))

            category_number_items = self._weapon_category_number_regex.findall(text_without_tags)

            for count, category in category_number_items:
                yield CategoryDTO[WeaponDTO](category=category.strip().lower(), count=int(count))
