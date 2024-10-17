import re
from typing import List

from tg_bot_float_common_dtos.csgo_database_source_dtos.weapons_page_dto import (
    WeaponsPageDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class WeaponsPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._weapon_regex = re.compile(self._settings.weapon_regex_pattern)

    async def get_weapon_names(self):
        response_text = await self._get_response(
            self._settings.base_url + self._settings.weapons_page
        )
        weapon_names = self._get_item_names(self._weapon_regex, response_text)
        return self._get_sorted_weapon_names_response(weapon_names)

    def _get_sorted_weapon_names_response(self, weapon_names: List[str]) -> WeaponsPageDTO:
        knife_index = weapon_names.index(self._settings.first_knife_weapon)
        other_index = weapon_names.index(self._settings.first_other_weapon)
        weapons: List[str] = weapon_names[:knife_index]
        knifes: List[str] = [f"★ {knife}" for knife in weapon_names[knife_index:other_index]]
        other: List[str] = weapon_names[other_index:]
        return WeaponsPageDTO(weapons=weapons, knives=knifes, other=other)
