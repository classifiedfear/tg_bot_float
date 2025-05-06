from typing import Annotated

from fastapi import Depends


from tg_bot_float_db_app.api.router_controllers.query_params.relation_id_request_dto import RelationIdRequestDTO
from tg_bot_float_db_app.api.router_controllers.query_params.relation_name_request_dto import RelationNameRequestDTO
from tg_bot_float_db_app.api.router_controllers.query_params.subscription_params import (
    SubscriptionParams,
)
from tg_bot_float_db_app.api.router_controllers.query_params.users_by_subscription_params import (
    UsersBySubscriptionParams,
)


SUBSCRIPTION_QUERY = Annotated[SubscriptionParams, Depends(SubscriptionParams)]

RELATION_ID_REQUEST = Annotated[RelationIdRequestDTO, Depends(RelationIdRequestDTO)]

RELATION_NAME_REQUEST = Annotated[RelationNameRequestDTO, Depends(RelationNameRequestDTO)]

USERS_BY_SUBSCIPTION_PARAMS = Annotated[
    UsersBySubscriptionParams, Depends(UsersBySubscriptionParams)
]
