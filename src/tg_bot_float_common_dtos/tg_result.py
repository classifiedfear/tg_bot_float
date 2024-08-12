from dataclasses import dataclass
from typing import List

from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.dtos.item_with_benefit_dto import (
    ItemWithBenefitDTO,
)
from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO


@dataclass
class TgResult:
    items_with_benefit: List[ItemWithBenefitDTO]
    subscription_info: FullSubscriptionDTO
