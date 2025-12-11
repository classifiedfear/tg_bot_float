from typing import Generator, List
import re
from itertools import islice


from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import CategoryWeaponsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser


class WeaponsParser(AbstractParser[WeaponsPageDTO]):
    def __init__(self, settings: ParserSettings) -> None:
        self._total_weapon_regex = re.compile(settings.total_weapon_regex)
        self._weapon_name_regex = re.compile(settings.weapon_name_regex)
        self._weapon_category_number_regex = re.compile(settings.weapon_category_number_regex)
        self._tags_regex = re.compile(r"<[^>]+>")

    def get_parsed_data(self, page_html: str) -> WeaponsPageDTO:
        if page_html == "":
            raise CsgoDbException("No weapons found!")

        weapon_dtos = self._get_weapon_dtos(page_html)
        return WeaponsPageDTO(
            categories=weapon_dtos, count=sum(map(lambda dto: dto.count, weapon_dtos))
        )

    def _get_weapon_dtos(self, page_html: str) -> List[CategoryWeaponsDTO]:
        weapon_dtos: List[CategoryWeaponsDTO] = []

        weapon_names_gen = self._get_iter_info(self._weapon_name_regex, page_html)

        for dto in self._get_weapon_dtos_without_names(page_html):
            names_chunk = list(islice(weapon_names_gen, dto.count))
            dto.weapons = names_chunk

            if dto.category == "heavy weapons":
                dto.category = "heavy"

            weapon_dtos.append(dto)

        if len(weapon_dtos) == 0:
            raise CsgoDbException("Wrong page request!")

        remaining_names = list(weapon_names_gen)

        if remaining_names:
            weapon_dtos.append(
                CategoryWeaponsDTO(
                    category="other", weapons=remaining_names, count=len(remaining_names)
                )
            )

        return weapon_dtos

    def _get_weapon_dtos_without_names(
        self, response_text: str
    ) -> Generator[CategoryWeaponsDTO, None, None]:
        total_weapon_text = self._total_weapon_regex.search(response_text)

        if total_weapon_text:

            text_without_tags = self._tags_regex.sub("", total_weapon_text.group(0))

            category_number_items = self._weapon_category_number_regex.findall(text_without_tags)

            for count, category in category_number_items:
                yield CategoryWeaponsDTO(category=category.strip().lower(), count=int(count))
