from typing import Annotated

from fastapi import Depends


class SubscriptionQuery:
    def __init__(
        self, telegram_id: int, weapon_id: int, skin_id: int, quality_id: int, stattrak: bool
    ):
        self.telegram_id = telegram_id
        self.weapon_id = weapon_id
        self.skin_id = skin_id
        self.quality_id = quality_id
        self.stattrak = stattrak


SUBSCRIPTION_QUERY = Annotated[SubscriptionQuery, Depends(SubscriptionQuery)]
