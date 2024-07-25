from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.links import Page

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_common_dtos.schema_dtos.subscription_to_find_dto import SubscriptionToFindDTO


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
            "/", self._get_all, methods=["GET"], response_model=Page[SubscriptionDTO]
        )
        self._router.add_api_route(
            "/tofind",
            self._get_subscription_by_valuables,
            methods=["GET"],
            response_model=Page[SubscriptionToFindDTO],
        )
        self._router.add_api_route(
            "/{telegram_id}/{weapon_id}/{skin_id}/{quality_id}/{stattrak}",
            self._get_subscription,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/{telegram_id}/{weapon_id}/{skin_id}/{quality_id}/{stattrak}",
            self._delete_subscribtion,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.router.add_api_route(
            "/{telegram_id}",
            self._get_subscriptions_by_telegram_id,
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

    async def _get_subscription(
        self, service_factory: BOT_DB_SERVICE_FACTORY, query: SUBSCRIPTION_QUERY
    ) -> SubscriptionModel:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_subscription(
                query.telegram_id, query.weapon_id, query.skin_id, query.quality_id, query.stattrak
            )

    async def _delete_subscribtion(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        query: SUBSCRIPTION_QUERY,
    ) -> None:
        async with service_factory:
            subsciption_service = service_factory.get_subscription_service()
            await subsciption_service.delete(
                query.telegram_id,
                query.weapon_id,
                query.skin_id,
                query.quality_id,
                query.stattrak,
            )

    async def _get_subscription_by_valuables(
        self, service_factory: BOT_DB_SERVICE_FACTORY
    ) -> Page[SubscriptionToFindDTO]:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_valuable_subscriptions()

    async def _get_subscriptions_by_telegram_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, telegram_id: int
    ) -> Page[SubscriptionModel]:
        async with service_factory:
            subscription_service = service_factory.get_subscription_service()
            return await subscription_service.get_subscriptions_by_telegram_id_paginated(
                telegram_id
            )
