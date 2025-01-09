import asyncio

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_common_dtos.tg_result_dtos.tg_result_dto import TgResultDTO
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.csm_steam_comparer import (
    CsmSteamComparer,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.dtos.csm_steam_items_to_compare_dto import (
    CsmSteamItemsToCompareDTO,
)

from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.result_sender_service import (
    ResultSenderService,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.csm_steam_source_data_getter import (
    CsmSteamSourceDataGetter,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.source_data_getter.subscription_source_data_getter import (
    SubscriptionSourceDataGetter,
)


class CsmSteamMarketBenefitFinderService:
    def __init__(
        self,
        csm_steam_source_data_getter: CsmSteamSourceDataGetter,
        subscription_source_data_getter: SubscriptionSourceDataGetter,
        csm_steam_comparer: CsmSteamComparer,
        result_sender_service: ResultSenderService,
    ):
        self._csm_steam_source_getter_service = csm_steam_source_data_getter
        self._subscription_source_getter_service = subscription_source_data_getter
        self._csm_steam_comparer = csm_steam_comparer
        self._result_sender_service = result_sender_service

    async def find_items_with_benefit(self) -> None:
        for subscription in await self._subscription_source_getter_service.get_user_subscriptions():
            items_to_compare = await self._try_find_items_to_compare(subscription)
            items_with_benefit = self._csm_steam_comparer.compare(items_to_compare)
            await self._result_sender_service.send(
                TgResultDTO(items_with_benefit=items_with_benefit, subscription_info=subscription)
            )
            await asyncio.sleep(5)

    async def _try_find_items_to_compare(
        self, subscription: SubscriptionToFindDTO
    ) -> CsmSteamItemsToCompareDTO:
        csm_items, steam_items = await asyncio.gather(
            self._csm_steam_source_getter_service.get_csm_items(subscription),
            self._csm_steam_source_getter_service.get_steam_items(subscription),
        )
        if not csm_items or not steam_items:
            return CsmSteamItemsToCompareDTO()
        return CsmSteamItemsToCompareDTO(csm_items, steam_items)
