from typing import List

from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.abstract_source_data_getter import (
    AbstractSourceDataGetter,
)


class CsmSteamMarketSourceDataGetter(AbstractSourceDataGetter):
    async def get_csm_market_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[CsmItemDTO]:
        csm_market_items: List[CsmItemDTO] = []
        current_link = self._settings.csm_base_url + self._settings.get_item_url.format(
            weapon=weapon,
            skin=skin,
            quality=quality,
            stattrak=stattrak,
        )
        offset = 0
        while True:
            offset_param = f"?offset={offset}"
            response_json = await self._get_response(current_link + offset_param)
            if isinstance(response_json, dict):
                break
            offset += 60
            csm_market_items.extend(
                [CsmItemDTO.model_validate(response_item) for response_item in response_json]
            )
        return csm_market_items

    async def get_steam_market_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[SteamItemDTO]:
        response_json = await self._get_response(
            self._settings.steam_base_url
            + self._settings.get_item_url.format(
                weapon=weapon,
                skin=skin,
                quality=quality,
                stattrak=stattrak,
            )
        )
        if isinstance(response_json, dict):
            return []
        return [SteamItemDTO.model_validate(response_item) for response_item in response_json]
