from fastapi import APIRouter, Query, Response, status
from fastapi_pagination.links import Page

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.api.dependencies.params import SUBSCRIPTION_QUERY
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO


class SubscriptionRouter(AbstractRouterController):
    def __init__(self):
        self._router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
        super().__init__()

    def _init_routes(self):
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[SubscriptionDTO]
        )
        self._router.add_api_route(
            "/tofind",
            self._get_by_valuables,
            methods=["GET"],
            response_model=Page[SubscriptionToFindDTO],
        )
        self._router.add_api_route(
            "/{telegram_id}/{weapon_id}/{skin_id}/{quality_id}/{stattrak}",
            self._get,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/{telegram_id}/{weapon_id}/{skin_id}/{quality_id}/{stattrak}",
            self._delete,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.router.add_api_route(
            "/{telegram_id}",
            self._get_by_telegram_id,
            methods=["GET"],
            response_model=Page[SubscriptionDTO],
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

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[SubscriptionModel]:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_all_paginated()

    async def _get(
        self, service_factory: BOT_DB_SERVICE_FACTORY, params: SUBSCRIPTION_QUERY = Query()
    ) -> SubscriptionModel:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_subscription(
                params.telegram_id,
                params.weapon_id,
                params.skin_id,
                params.quality_id,
                params.stattrak,
            )

    async def _delete(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        params: SUBSCRIPTION_QUERY = Query(),
    ) -> None:
        async with service_factory:
            subsciption_service = service_factory.get_subscription_service()
            await subsciption_service.delete(
                params.telegram_id,
                params.weapon_id,
                params.skin_id,
                params.quality_id,
                params.stattrak,
            )

    async def _get_by_valuables(
        self, service_factory: BOT_DB_SERVICE_FACTORY
    ) -> Page[SubscriptionToFindDTO]:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_valuable_subscriptions()

    async def _get_by_telegram_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, telegram_id: int
    ) -> Page[SubscriptionModel]:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_subscriptions_by_telegram_id_paginated(
                telegram_id
            )
