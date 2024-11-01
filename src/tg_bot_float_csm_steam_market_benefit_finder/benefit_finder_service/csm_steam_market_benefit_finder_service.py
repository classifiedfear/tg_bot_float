import asyncio

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.tg_result_dtos.tg_result_dto import TgResultDTO
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder_service.csm_steam_comparer import (
    CsmSteamComparer,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder_service.dtos.csm_steam_items_to_compare_dto import (
    CsmSteamItemsToCompareDTO,
)

from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder_service.result_sender_service import (
    ResultSenderService,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder_service.source_getter_service.csm_steam_source_getter_service import (
    CsmSteamSourceGetterService,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder_service.source_getter_service.subscription_source_servive import (
    SubscriptionSourceGetterService,
)


class CsmSteamMarketBenefitFinderService:
    def __init__(
        self,
        subscription_source_getter_service: SubscriptionSourceGetterService,
        csm_steam_source_getter_service: CsmSteamSourceGetterService,
        result_sender_service: ResultSenderService,
        csm_steam_comparer: CsmSteamComparer,
    ):
        self._subscription_source_getter_service = subscription_source_getter_service
        self._csm_steam_source_getter_service = csm_steam_source_getter_service
        self._result_sender_service = result_sender_service
        self._csm_steam_comparer = csm_steam_comparer

    async def find_items_with_benefit(self) -> None:
        for subscription in await self._subscription_source_getter_service.get_user_subscriptions():
            item_to_find = (
                await self._subscription_source_getter_service.get_weapon_skin_quality_names(
                    subscription
                )
            )
            items_to_compare = await self._try_find_items_to_compare(item_to_find)
            items_with_benefit = self._csm_steam_comparer.compare(items_to_compare)
            await self._result_sender_service.send(
                TgResultDTO(items_with_benefit=items_with_benefit, subscription_info=item_to_find)
            )
            await asyncio.sleep(5)

    async def _try_find_items_to_compare(
        self, subscription: FullSubscriptionDTO
    ) -> CsmSteamItemsToCompareDTO:
        csm_items, steam_items = await asyncio.gather(
            self._csm_steam_source_getter_service.get_csm_items(subscription),
            self._csm_steam_source_getter_service.get_steam_items(subscription),
        )
        if not csm_items or not steam_items:
            return CsmSteamItemsToCompareDTO()
        return CsmSteamItemsToCompareDTO(csm_items, steam_items)
