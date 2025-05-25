from tg_bot_float_telegram_app.service_client.sub_requests_service_client_mixin import (
    SubRequestsServiceClientMixin,
)
from tg_bot_float_telegram_app.service_client.user_requests_service_client_mixin import (
    UserRequestsServiceClientMixin,
)
from tg_bot_float_telegram_app.service_client.wsq_requests_service_client_mixin import (
    WSQRequestsServiceClientMixin,
)


class DbAppServiceClient(
    UserRequestsServiceClientMixin,
    SubRequestsServiceClientMixin,
    WSQRequestsServiceClientMixin,
):
    pass
