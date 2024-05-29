from fastapi import APIRouter, Response, status
from fastapi_pagination.links import Page

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel


class SubscriptionRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[SubscriptionModel]
        )
    async def _create(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        subscription_dto: SubscriptionDTO,
        response: Response,
    ) -> None:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            subscription_db_model = await subscription_service.create(subscription_dto)
            response.headers["Location"] = f"/subscriptions/id/{subscription_db_model.id}"

    async def _get_all(self, service_fatory: BOT_DB_SERVICE_FACTORY) -> Page[SubscriptionModel]:
        async with service_fatory:
            subscription_service = service_fatory.get_subscription_service()
            return await subscription_service.get_all()
