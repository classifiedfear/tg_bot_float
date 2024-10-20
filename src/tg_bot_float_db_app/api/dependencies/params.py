from typing import Annotated

from fastapi import Depends

from tg_bot_float_db_app.api.router_controllers.params.subscription_params import SubscriptionParams
from tg_bot_float_db_app.api.router_controllers.params.users_by_subscription_params import (
    UsersBySubscriptionParams,
)


SUBSCRIPTION_QUERY = Annotated[SubscriptionParams, Depends(SubscriptionParams)]

USERS_BY_SUBSCIPTION_PARAMS = Annotated[
    UsersBySubscriptionParams, Depends(UsersBySubscriptionParams)
]
