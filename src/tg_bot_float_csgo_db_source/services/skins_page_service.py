import re
from tg_bot_float_common_dtos.csgo_database_source_dtos.skins_page_response_dto import (
    SkinsPageResponseDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class SkinsPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._skin_regex = re.compile(self._settings.skin_regex_pattern)

    async def get_skin_names(self, item_name: str) -> SkinsPageResponseDTO:
        response_text = await self._get_response(
            self._settings.base_url + self._settings.skins_page.format(weapon=item_name)
        )
        skin_names = self._get_item_names(self._skin_regex, response_text)
        if skin_names and skin_names[0] == "Vanilla":
            return SkinsPageResponseDTO(weapon_name=item_name, skins=skin_names[1:])
        return SkinsPageResponseDTO(weapon_name=item_name, skins=skin_names)
