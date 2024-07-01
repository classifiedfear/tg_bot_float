import re
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings
from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class WeaponPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._weapon_regex = re.compile(self._settings.weapon_regex_pattern)

    async def get_weapon_names(self):
        weapon_names = await self._get_item_names(
            self._settings.base_url + self._settings.weapons_page,
            self._weapon_regex,
        )
        knife_index = float("inf")
        for index, weapon_name in enumerate(weapon_names):
            if index < knife_index:
                if weapon_name == "Negev":
                    knife_index = index + 1
            else:
                weapon_names[index] = f"★ {weapon_name}"
        return weapon_names
