from typing import Any, Dict, List, Tuple
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
        self._collection_regex = re.compile(settings.collection_regex)

    def get_parsed_data(self, page_html: str) -> AdditionalInfoPageDTO:
        additional_info_page_dto: Dict[str, Any] = {}

        additional_info_page_dto["weapon_name"], additional_info_page_dto["skin_name"] = (
            self._get_weapon_skin_name(page_html)
        )

        if rarity := self._extract_regex(self._rarity_regex, page_html):
            additional_info_page_dto["rarity"] = rarity

        quality_stattrak_dto = self._get_quality_stattrak_dto(page_html)

        additional_info_page_dto["qualities"], additional_info_page_dto["stattrak_existence"] = (
            quality_stattrak_dto.qualities,
            quality_stattrak_dto.stattrak_existence,
        )

        return AdditionalInfoPageDTO.model_validate(additional_info_page_dto)

    def _get_weapon_skin_name(self, page_html: str) -> Tuple[str, str]:
        if weapon_skin_name := self._extract_regex(
            self._additional_weapon_skin_name_regex,
            page_html,
        ):
            weapon, sep, skin = weapon_skin_name.partition("|")  # type: ignore
            return weapon.strip(), skin.strip()
        raise CsgoDbException("Weapon not found in HTML")

    def _extract_regex(self, pattern: re.Pattern[str], page_html: str) -> str | None:
        if match := pattern.search(page_html):
            return match.group(1)
        return None

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

        primary_qualities = stattrak_qualities or qualities

        return QualityStattrakDTO(
            qualities=primary_qualities,
            stattrak_existence=bool(stattrak_qualities),
        )
