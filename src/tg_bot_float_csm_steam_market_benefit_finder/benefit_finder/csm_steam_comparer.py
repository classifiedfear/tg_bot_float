from collections import defaultdict
from decimal import Decimal, localcontext
from typing import Dict, List

from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_common_dtos.tg_result_dtos.item_with_benefit_dto import (
    ItemWithBenefitDTO,
)
from tg_bot_float_csm_steam_market_benefit_finder.benefit_finder.dtos.csm_steam_items_to_compare_dto import (
    CsmSteamItemsToCompareDTO,
)


class CsmSteamComparer:
    def compare(self, items_to_compare: CsmSteamItemsToCompareDTO):
        with localcontext() as context:
            context.prec = 2
            dict_steam_items = self._get_dict_steam_items(items_to_compare.steam_items)
            dict_csm_items = self._get_dict_csm_items(items_to_compare.csm_items)
            return self._find_benefit_items(dict_csm_items, dict_steam_items)

    @staticmethod
    def _get_dict_steam_items(
        steam_items: List[SteamItemDTO],
    ) -> Dict[Decimal, List[SteamItemDTO]]:
        dict_steam_items: Dict[Decimal, List[SteamItemDTO]] = defaultdict(list)
        for item_dto in steam_items:
            steam_float = Decimal(item_dto.item_float) * 1
            dict_steam_items[steam_float].append(item_dto)
        return dict_steam_items

    @staticmethod
    def _get_dict_csm_items(csm_items: List[CsmItemDTO]) -> Dict[Decimal, List[CsmItemDTO]]:
        dict_csm_items: Dict[Decimal, List[CsmItemDTO]] = defaultdict(list)
        for item_dto in csm_items:
            csm_float = Decimal(item_dto.item_float) * 1
            dict_csm_items[csm_float].append(item_dto)
        return dict_csm_items

    def _find_benefit_items(
        self,
        dict_csm_items: Dict[Decimal, List[CsmItemDTO]],
        dict_steam_items: Dict[Decimal, List[SteamItemDTO]],
    ) -> List[ItemWithBenefitDTO]:
        result: List[ItemWithBenefitDTO] = []
        for csm_float in dict_csm_items.keys():
            if (steam_items := dict_steam_items.get(csm_float)) is not None:
                csm_items = dict_csm_items[csm_float]
                max_benefit_item = self._find_max_benefit_item(csm_items, steam_items)
                if max_benefit_item:
                    result.append(max_benefit_item)
        return result

    def _find_max_benefit_item(
        self, csm_items: List[CsmItemDTO], steam_items: List[SteamItemDTO]
    ) -> ItemWithBenefitDTO | None:
        benefit_items: List[ItemWithBenefitDTO] = []
        for csm_item in csm_items:
            for steam_item in steam_items:
                if (percent := self._find_percent(csm_item, steam_item)) >= 10:
                    benefit_items.append(
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
                    )
        return (
            max(benefit_items, key=lambda matched: matched.benefit_percent)
            if benefit_items
            else None
        )

    @staticmethod
    def _find_percent(csm_skin: CsmItemDTO, steam_skin: SteamItemDTO):
        return int(100 - ((steam_skin.price * 100) // csm_skin.price_with_float))
