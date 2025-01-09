from dataclasses import dataclass
from typing import List

from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO
from tg_bot_float_common_dtos.tg_result_dtos.item_with_benefit_dto import (
    ItemWithBenefitDTO,
)


@dataclass
class TgResultDTO:
    items_with_benefit: List[ItemWithBenefitDTO]
    subscription_info: SubscriptionToFindDTO
