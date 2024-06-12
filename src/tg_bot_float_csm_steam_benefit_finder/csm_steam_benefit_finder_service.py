from collections import defaultdict
from decimal import localcontext, Decimal
from typing import Dict, List

from tg_bot_float_csm_steam_benefit_finder.items_to_compare import ItemsToCompareDTO
from tg_bot_float_csm_steam_benefit_finder.source_data_getter_service import SourceDataGetterService
from tg_bot_float_csm_steam_benefit_finder.item_with_benefit_dto import ItemWithBenefitDTO
from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO


class CsmSteamBenefitFinderService:
    def __init__(self, source_data_getter_service: SourceDataGetterService):
        self._count = -1
        self._source_data_getter_service = source_data_getter_service

    async def find_items_with_benefit(self):
        async with self._source_data_getter_service:
            weapon, skin, quality, stattrak = await self._get_item_to_find()
            items_to_compare = await self._try_find_items_to_compare(
                weapon, skin, quality, stattrak
            )
        return await self._try_to_find_items_with_benefit(items_to_compare)

    async def _get_item_to_find(self):
        subscriptions = await self._source_data_getter_service.get_user_subscriptions()
        # temporary solution
        if self._count == -1:
            self._count = len(subscriptions) - 1
        else:
            self._count -= 1
        subscription = subscriptions[self._count]
        ###############
        item_to_find = await self._source_data_getter_service.get_weapon_skin_quality_names(
            subscription["weapon_id"],
            subscription["skin_id"],
            subscription["quality_id"],
        )
        return (
            item_to_find["weapon"],
            item_to_find["skin"],
            item_to_find["quality"],
            subscription["stattrak"],
        )

    async def _try_find_items_to_compare(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> ItemsToCompareDTO:
        csm_items = await self._source_data_getter_service.get_csm_items(
            weapon, skin, quality, stattrak
        )
        steam_items = await self._source_data_getter_service.get_steam_items(
            weapon, skin, quality, stattrak
        )
        if not (csm_items or steam_items):
            return ItemsToCompareDTO()
        csm_items = [CsmItemResponseDTO.model_validate(item) for item in csm_items]
        steam_items = [SteamItemResponseDTO.model_validate(item) for item in steam_items]
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
        steam_items: List[SteamItemResponseDTO],
    ) -> Dict[Decimal, List[SteamItemResponseDTO]]:
        grouped_by_float: Dict[Decimal, List[SteamItemResponseDTO]] = defaultdict(list)
        for steam_item_dto in steam_items:
            steam_float = Decimal(steam_item_dto.item_float) * 1
            grouped_by_float[steam_float].append(steam_item_dto)
        return grouped_by_float

    async def _compare(
        self,
        csm_items: List[CsmItemResponseDTO],
        steam_items: Dict[Decimal, List[SteamItemResponseDTO]],
    ):
        result: List[ItemWithBenefitDTO] = []
        for csm_item in csm_items:
            if (
                steam_csm_match_dto := self._try_to_find_by_find(csm_item, steam_items)
            ) is not None:
                result.append(steam_csm_match_dto)
        return result

    def _try_to_find_by_find(
        self, csm_skin: CsmItemResponseDTO, steam_skins: Dict[Decimal, List[SteamItemResponseDTO]]
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
    def _try_to_find_by_float(
        csm_skin: CsmItemResponseDTO, steam_skins: Dict[Decimal, List[SteamItemResponseDTO]]
    ):
        csm_float = Decimal(csm_skin.item_float) * 1
        return steam_skins.get(csm_float)

    def _try_to_find_by_percent(
        self, csm_item: CsmItemResponseDTO, matched_by_float_steam_skins: List[SteamItemResponseDTO]
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
    def _find_percent(csm_skin: CsmItemResponseDTO, steam_skin: SteamItemResponseDTO):
        return int(100 - ((steam_skin.price * 100) // csm_skin.price_with_float))
