from typing import List

from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.abstract_source_data_getter import (
    AbstractSourceDataGetter,
)
from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO


class CsmSteamSourceDataGetter(AbstractSourceDataGetter):
    async def get_csm_items(self, subscription: SubscriptionToFindDTO) -> List[CsmItemDTO]:
        csm_items: List[CsmItemDTO] = []
        current_link = self._settings.csm_base_url + self._settings.get_item_url.format(
            weapon=subscription.weapon_name,
            skin=subscription.skin_name,
            quality=subscription.quality_name,
            stattrak=subscription.stattrak,
        )
        offset = 0
        while True:
            response_json = await self._get_response(current_link + f"?offset={offset}")
            offset += 60
            if isinstance(response_json, dict):
                break
            csm_items.extend([CsmItemDTO.model_validate(item) for item in response_json])
        return csm_items

    async def get_steam_items(self, subscription: SubscriptionToFindDTO) -> List[SteamItemDTO]:
        response_json = await self._get_response(
            self._settings.steam_base_url
            + self._settings.get_item_url.format(
                weapon=subscription.weapon_name,
                skin=subscription.skin_name,
                quality=subscription.quality_name,
                stattrak=subscription.stattrak,
            )
        )
        if isinstance(response_json, dict):
            return []
        return [SteamItemDTO.model_validate(item) for item in response_json]
