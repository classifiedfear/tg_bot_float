from typing import List

from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.abstract_source_getter_service import (
    AbstractSourceGetterService,
)


class CsgoDbSourceGetterService(AbstractSourceGetterService):

    async def get_weapon_names(self) -> List[str]:
        return await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_weapons_url
        )

    async def get_skin_names(self, weapon: str) -> List[str]:
        return await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_skins_url.format(weapon=weapon)
        )
