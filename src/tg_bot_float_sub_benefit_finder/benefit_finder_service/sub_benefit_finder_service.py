import asyncio

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.tg_result import TgResult
from tg_bot_float_sub_benefit_finder.benefit_finder_service.csm_steam_comparer import (
    CsmSteamComparer,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.dtos.items_to_compare_dto import (
    ItemsToCompareDTO,
)
from tg_bot_float_sub_benefit_finder.benefit_finder_service.source_data_getter_service import (
    SourceDataGetterService,
)

from tg_bot_float_sub_benefit_finder.benefit_finder_service.result_sender_service import (
    ResultSenderService,
)


class SubBenefitFinderService:
    def __init__(
        self,
        source_data_getter_service: SourceDataGetterService,
        benefit_sender_service: ResultSenderService,
        csm_steam_comparer: CsmSteamComparer,
    ):
        self._source_data_getter_service = source_data_getter_service
        self._benefit_sender_service = benefit_sender_service
        self._csm_steam_comparer = csm_steam_comparer

    async def find_items_with_benefit(self):
        for subscription in await self._source_data_getter_service.get_user_subscriptions():
            item_to_find = await self._source_data_getter_service.get_weapon_skin_quality_names(
                subscription
            )
            items_to_compare = await self._try_find_items_to_compare(item_to_find)
            items_with_benefit = self._csm_steam_comparer.compare(items_to_compare)
            await self._benefit_sender_service.send(items_with_benefit)
            await asyncio.sleep(5)

    async def _try_find_items_to_compare(
        self, subscription: FullSubscriptionDTO
    ) -> ItemsToCompareDTO:
        csm_items, steam_items = await asyncio.gather(
            self._source_data_getter_service.get_csm_items(subscription),
            self._source_data_getter_service.get_steam_items(subscription),
        )
        if not csm_items or not steam_items:
            return ItemsToCompareDTO()
        return ItemsToCompareDTO(csm_items, steam_items)
