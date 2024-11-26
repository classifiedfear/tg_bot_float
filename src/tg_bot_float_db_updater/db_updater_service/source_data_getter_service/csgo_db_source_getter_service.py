from typing import List
from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.abstract_source_getter_service import (
    AbstractSourceGetterService,
)


class CsgoDbSourceGetterService(AbstractSourceGetterService):

    async def get_weapons_page(self) -> WeaponsPageDTO:
        json_response = await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_weapons_url
        )
        return WeaponsPageDTO.model_validate(json_response)

    async def get_skins_page(self, weapon: str) -> SkinsPageDTO:
        json_response = await self._get_response(
            self._settings.csgo_db_url
            + self._settings.csgo_db_skins_url.format(
                weapon=weapon.lower().replace("★ ", "").replace(" ", "-")
            )
        )
        if message := json_response.get("message"):
            return SkinsPageDTO(weapon_name=message, skins=[])
        return SkinsPageDTO.model_validate(json_response)

    async def get_gloves_page(self) -> List[GlovesPageDTO]:
        json_response = await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_gloves_url
        )
        return [GlovesPageDTO.model_validate(item) for item in json_response]

    async def get_agents_page(self) -> List[AgentsPageDTO]:
        json_response = await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_agents_url
        )
        return [AgentsPageDTO.model_validate(item) for item in json_response]