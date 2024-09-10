from dataclasses import dataclass
from typing import List


from tg_bot_float_common_dtos.tg_result_dtos.item_with_benefit_dto import ItemWithBenefitDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO


@dataclass
class TgResultDTO:
    items_with_benefit: List[ItemWithBenefitDTO]
    subscription_info: SubscriptionDTO
