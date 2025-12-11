from typing import List, Tuple
import re

from tg_bot_float_common_dtos.csgo_db_source_dtos.additional_info_page_dto import (
    AdditionalInfoPageDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.abstract_parser import AbstractParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings
from tg_bot_float_csgo_db_source.dtos.quality_stattrak_dto import QualityStattrakDTO


class AdditionalInfoParser(AbstractParser[AdditionalInfoPageDTO]):
    def __init__(self, settings: ParserSettings) -> None:
        self._quality_stattrak_regex = re.compile(settings.quality_stattrak_regex)
        self._additional_weapon_skin_name_regex = re.compile(
            settings.additional_weapon_skin_name_regex
        )
        self._rarity_regex = re.compile(settings.rarity_regex)

    def get_parsed_data(self, page_html: str) -> AdditionalInfoPageDTO:
        if page_html == "":
            raise CsgoDbException("No additional info found!")

        weapon_name, skin_name = self._get_weapon_skin_name(page_html)

        rarity = self._extract_regex(self._rarity_regex, page_html)

        quality_stattrak_dto = self._get_quality_stattrak_dto(page_html)

        return AdditionalInfoPageDTO(
            weapon_name=weapon_name,
            skin_name=skin_name,
            qualities=quality_stattrak_dto.qualities,
            stattrak_qualities=quality_stattrak_dto.stattrak_qualities,
            stattrak_existence=quality_stattrak_dto.stattrak_existence,
            rarity=rarity if rarity is not None else "Extraordinary",
        )

    def _get_weapon_skin_name(self, page_html: str) -> Tuple[str, str]:
        if weapon_skin_name := self._extract_regex(
            self._additional_weapon_skin_name_regex,
            page_html,
        ):
            weapon, sep, skin = weapon_skin_name.partition("|")  # type: ignore
            return weapon.strip(), skin.strip()
        raise CsgoDbException("Weapon not found in HTML")

    def _get_quality_stattrak_dto(self, page_html: str) -> QualityStattrakDTO:
        stattrak_qualities: List[str] = []
        qualities: List[str] = []

        for match in self._quality_stattrak_regex.finditer(page_html):
            stattrak_match = match.group(1)
            quality_match = match.group(2)

            if stattrak_match:
                stattrak_qualities.append(stattrak_match)

            if quality_match:
                qualities.append(quality_match)

        return QualityStattrakDTO(
            qualities=qualities,
            stattrak_qualities=stattrak_qualities,
            stattrak_existence=bool(stattrak_qualities),
        )
