import asyncio
from typing import List
from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_db_updater.db_updater.source_data_getter.abstract_source_data_getter import (
    AbstractSourceGetter,
)


class CsgoDbSourceDataGetter(AbstractSourceGetter):

    async def get_weapons_page(self) -> WeaponsPageDTO:
        json_response = await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_weapons_url
        )
        return WeaponsPageDTO.model_validate(json_response)

    async def get_skins_page(self, weapon: str) -> SkinsPageDTO:
        weapon_name = weapon.lower().replace("★ ", "").replace(" ", "-")
        while True:
            json_response = await self._get_response(
                self._settings.csgo_db_url
                + self._settings.csgo_db_skins_url.format(weapon=weapon_name)
            )
            skins_page_dto = SkinsPageDTO.model_validate(json_response)
            if skins_page_dto.skins:
                print(f"Found skins for weapon: {weapon_name}")
                print(f"Number of skins: {len(skins_page_dto.skins)}")
                return skins_page_dto
            await asyncio.sleep(1)  # Wait before retrying

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
