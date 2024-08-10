import asyncio
from collections import defaultdict
from decimal import localcontext, Decimal
from typing import Dict, List

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find import SubscriptionToFindDTO
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.items_to_compare_dto import (
    ItemsToCompareDTO,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.source_data_getter_service import (
    SourceDataGetterService,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.item_with_benefit_dto import (
    ItemWithBenefitDTO,
)
from tg_bot_float_common_dtos.source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.csm_steam_benefit_sender_service import (
    CsmSteamBenefitSenderService,
)
from tg_bot_float_common_dtos.benefit_result import BenefitResultDTO


class CsmSteamBenefitFinderService:
    def __init__(
        self,
        source_data_getter_service: SourceDataGetterService,
        benefit_sender_service: CsmSteamBenefitSenderService,
    ):
        self._source_data_getter_service = source_data_getter_service
        self._benefit_sender_service = benefit_sender_service

    async def find_items_with_benefit(self, subscription_dtos: List[SubscriptionToFindDTO]):
        subscription = await self._get_subscription_to_find(subscription_dtos)
        items_to_compare = await self._try_find_items_to_compare(subscription)
        items_with_benefit = await self._try_to_find_items_with_benefit(items_to_compare)
        print(
            BenefitResultDTO(items_with_benefit=items_with_benefit, subscription_info=subscription)
        )
        # await self._benefit_sender_service.send(items_with_benefit)

    async def _get_subscription_to_find(
        self, subscription_dtos: List[SubscriptionToFindDTO]
    ) -> FullSubscriptionDTO:
        if not subscription_dtos:
            for sub in await self._source_data_getter_service.get_user_subscriptions():
                subscription_dtos.append(sub)
            subscription = subscription_dtos.pop(0)
        else:
            subscription = subscription_dtos.pop(0)
        item_to_find = await self._source_data_getter_service.get_weapon_skin_quality_names(
            subscription
        )
        return item_to_find

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

    async def _try_to_find_items_with_benefit(
        self,
        items_to_compare: ItemsToCompareDTO,
    ):
        with localcontext() as context:
            context.prec = 2
            grouped_items_by_float = self._get_grouped_items_by_float(items_to_compare.steam_items)
            return await self._compare(items_to_compare.csm_items, grouped_items_by_float)

    @staticmethod
    def _get_grouped_items_by_float(
        steam_items: List[SteamItemDTO],
    ) -> Dict[Decimal, List[SteamItemDTO]]:
        grouped_by_float: Dict[Decimal, List[SteamItemDTO]] = defaultdict(list)
        for steam_item_dto in steam_items:
            steam_float = Decimal(steam_item_dto.item_float) * 1
            grouped_by_float[steam_float].append(steam_item_dto)
        return grouped_by_float

    async def _compare(
        self,
        csm_items: List[CsmItemDTO],
        steam_items: Dict[Decimal, List[SteamItemDTO]],
    ):
        result: List[ItemWithBenefitDTO] = []
        for csm_item in csm_items:
            if (
                steam_csm_match_dto := self._try_to_find_by_find(csm_item, steam_items)
            ) is not None:
                result.append(steam_csm_match_dto)
        return result

    def _try_to_find_by_find(
        self, csm_skin: CsmItemDTO, steam_skins: Dict[Decimal, List[SteamItemDTO]]
    ):
        if matched_by_float_steam_skins := self._try_to_find_by_float(csm_skin, steam_skins):
            if matched_by_percent := self._try_to_find_by_percent(
                csm_skin, matched_by_float_steam_skins
            ):
                return max(
                    matched_by_percent, key=lambda matched_skin: matched_skin.benefit_percent
                )
        return None

    @staticmethod
    def _try_to_find_by_float(csm_skin: CsmItemDTO, steam_skins: Dict[Decimal, List[SteamItemDTO]]):
        csm_float = Decimal(csm_skin.item_float) * 1
        return steam_skins.get(csm_float)

    def _try_to_find_by_percent(
        self, csm_item: CsmItemDTO, matched_by_float_steam_skins: List[SteamItemDTO]
    ) -> List[ItemWithBenefitDTO]:
        return [
            ItemWithBenefitDTO(
                steam_item.name,
                steam_item.item_float,
                steam_item.price,
                steam_item.buy_link,
                csm_item.item_float,
                csm_item.price,
                csm_item.price_with_float,
                csm_item.overpay_float,
                percent,
            )
            for steam_item in matched_by_float_steam_skins
            if (percent := self._find_percent(csm_item, steam_item)) >= 10
        ]

    @staticmethod
    def _find_percent(csm_skin: CsmItemDTO, steam_skin: SteamItemDTO):
        return int(100 - ((steam_skin.price * 100) // csm_skin.price_with_float))
