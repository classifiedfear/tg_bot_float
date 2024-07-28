from typing import Annotated

from fastapi import Depends

from tg_bot_float_db_app.api.routers.params.subscription_params import SubscriptionParams


SUBSCRIPTION_QUERY = Annotated[SubscriptionParams, Depends(SubscriptionParams)]
