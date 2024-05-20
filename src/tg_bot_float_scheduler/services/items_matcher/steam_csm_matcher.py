from collections import defaultdict
from decimal import localcontext, Decimal
from typing import Dict, List

from tg_bot_float_scheduler.services.items_matcher.db_source_data_getter_service import (
    SourceDataGetterService,
)
from tg_bot_float_scheduler.services.items_matcher.steam_csm_match_dto import SteamCsmMatchDTO

from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO


class SteamCsmMatcher:
    def __init__(self, source_data_getter_service: SourceDataGetterService):
        self._source_data_getter_service = source_data_getter_service

    async def match(self, weapon: str, skin: str, quality: str, stattrak: bool):
        async with self._source_data_getter_service:
            csm_items = await self._source_data_getter_service.get_csm_items(
                weapon, skin, quality, stattrak
            )
            steam_items = await self._source_data_getter_service.get_steam_items(
                weapon, skin, quality, stattrak
            )
        if not (csm_items or steam_items):
            return
        csm_items = [CsmItemResponseDTO.model_validate(item) for item in csm_items]
        steam_items = [SteamItemResponseDTO.model_validate(item) for item in steam_items]
        return await self._get_matching_skins(csm_items, steam_items)

    async def _get_matching_skins(
        self, csm_items: List[CsmItemResponseDTO], steam_items: List[SteamItemResponseDTO]
    ):
        with localcontext() as context:
            context.prec = 2
            steam_dict_items = self._create_dict_by_floats(steam_items)
            return await self._compare(csm_items, steam_dict_items)

    @staticmethod
    def _create_dict_by_floats(
        steam_items: List[SteamItemResponseDTO],
    ) -> Dict[Decimal, List[SteamItemResponseDTO]]:
        floats_steam_dto: Dict[Decimal, List[SteamItemResponseDTO]] = defaultdict(list)
        for steam_item_dto in steam_items:
            steam_float = Decimal(steam_item_dto.item_float) * 1
            floats_steam_dto[steam_float].append(steam_item_dto)
        return floats_steam_dto

    async def _compare(
        self,
        csm_items: List[CsmItemResponseDTO],
        steam_items: Dict[Decimal, List[SteamItemResponseDTO]],
    ):
        result: List[SteamCsmMatchDTO] = []
        for csm_item in csm_items:
            if (
                steam_csm_match_dto := self._get_max_matched_skin_if_exists(csm_item, steam_items)
            ) is not None:
                result.append(steam_csm_match_dto)
        return result

    def _get_max_matched_skin_if_exists(
        self, csm_skin: CsmItemResponseDTO, steam_skins: Dict[Decimal, List[SteamItemResponseDTO]]
    ):
        if matched_by_float_steam_skins := self._get_matched_steam_skins_by_float_if_exists(
            csm_skin, steam_skins
        ):
            if matched_by_percent := self._get_csm_steam_matched_by_percent(
                csm_skin, matched_by_float_steam_skins
            ):
                return max(matched_by_percent, key=lambda matched_skin: matched_skin.percent)
        return None

    @staticmethod
    def _get_list_without_none_values(skins: List[SteamCsmMatchDTO]):
        return [skin for skin in skins if skin]

    @staticmethod
    def _get_matched_steam_skins_by_float_if_exists(
        csm_skin: CsmItemResponseDTO, steam_skins: Dict[Decimal, List[SteamItemResponseDTO]]
    ):
        csm_float = Decimal(csm_skin.item_float) * 1
        return steam_skins.get(csm_float)

    def _get_csm_steam_matched_by_percent(
        self, csm_skin: CsmItemResponseDTO, matched_by_float_steam_skins: List[SteamItemResponseDTO]
    ) -> List[SteamCsmMatchDTO]:
        return [
            SteamCsmMatchDTO(steam_skin, csm_skin, percent)
            for steam_skin in matched_by_float_steam_skins
            if (percent := self._find_percent(csm_skin, steam_skin)) >= 10
        ]

    @staticmethod
    def _find_percent(csm_skin: CsmItemResponseDTO, steam_skin: SteamItemResponseDTO):
        return int(100 - ((steam_skin.price * 100) // csm_skin.price_with_float))
