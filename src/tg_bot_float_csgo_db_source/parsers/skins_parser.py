from typing import List
import re
from itertools import islice
from collections import Counter

from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import WeaponSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


class SkinsParser(AbstractParser[SkinsPageDTO]):
    def __init__(self, settings: ParserSettings) -> None:
        self._skin_name_regex = re.compile(settings.skin_name_regex)
        self._skin_weapon_name_regex = re.compile(settings.skin_weapon_name_regex)
        self._skin_rarity_regex = re.compile(settings.skin_rarity_regex)

    def _get_correct_weapon_name(self, page_html: str) -> str:
        if weapon_name := self._extract_regex(self._skin_weapon_name_regex, page_html):
            return weapon_name
        raise CsgoDbException("Weapon not found in HTML")

    def get_parsed_data(self, page_html: str) -> SkinsPageDTO:
        if page_html == "":
            raise CsgoDbException("No skins found!")

        skin_dtos = self._get_skin_dtos(page_html)
        return SkinsPageDTO(
            weapon_name=skin_dtos[0].weapon_name,
            skins=skin_dtos,
            count=sum(map(lambda dto: dto.count, skin_dtos)),
        )

    def _get_skin_dtos(self, page_html: str) -> List[WeaponSkinsDTO]:
        weapon_skins_dtos: List[WeaponSkinsDTO] = []

        skin_names_gen = self._get_iter_info(self._skin_name_regex, page_html)

        rarity_counter: Counter[str] = self._count_rarity(page_html)

        correct_weapon_name = self._get_correct_weapon_name(page_html)

        for rarity, count in rarity_counter.items():
            names_chunk = list(islice(skin_names_gen, count))

            weapon_skin_dto = WeaponSkinsDTO(
                weapon_name=correct_weapon_name,
                skins=names_chunk,
                rarity=rarity,
                count=count,
            )

            if weapon_skin_dto.skins and weapon_skin_dto.skins[0] == "Vanilla":
                weapon_skin_dto.skins.pop(0)
                weapon_skin_dto.count -= 1

            weapon_skins_dtos.append(weapon_skin_dto)

        return weapon_skins_dtos

    def _count_rarity(self, response_text: str) -> Counter[str]:
        return Counter(match.group(1) for match in self._skin_rarity_regex.finditer(response_text))
