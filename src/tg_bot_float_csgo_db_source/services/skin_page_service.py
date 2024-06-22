import re
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class SkinPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._skin_regex = re.compile(self._settings.skin_regex_pattern)

    async def get_skin_names(self, weapon: str):
        if weapon[0] == "★":
            skin_names = await self._get_item_names(
                self._settings.base_url + self._settings.skins_page.format(weapon=weapon[2:]),
                self._skin_regex,
            )
        else:
            skin_names = await self._get_item_names(
                self._settings.base_url + self._settings.skins_page.format(weapon=weapon),
                self._skin_regex,
            )
        return skin_names[1:]
