from fastapi import APIRouter, Query, Response, status
from fastapi_pagination.links import Page

from tg_bot_float_common_dtos.schema_dtos.user_dto import UserDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.api.dependencies.params import USERS_BY_SUBSCIPTION_PARAMS
from tg_bot_float_db_app.database.models.user_model import UserModel
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)


class UserRouterController(AbstractRouterController):
    def __init__(self):
        self._router = APIRouter(prefix="/users", tags=["users"])
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/create",
            self._create,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/id/{user_id}", self._get_by_id, response_model=None, methods=["Get"]
        )
        self._router.add_api_route(
            "/id/{user_id}",
            self._update_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{user_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/telegram_id/{telegram_id}",
            self._get_by_telegram_id,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/telegram_id/{telegram_id}",
            self._delete_by_telegram_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[UserDTO]
        )
        self._router.add_api_route(
            "/users_by_subscription/{weapon_id}/{skin_id}/{quality_id}/{stattrak}",
            self._get_by_subscription,
            methods=["GET"],
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, user_dto: UserDTO
    ) -> None:
        async with service_factory:
            user_service = service_factory.get_user_service()
            user_db_model = await user_service.create(user_dto)
            response.headers["Location"] = f"/users/id/{user_db_model.id}"

    async def _get_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, user_id: int) -> UserModel:
        async with service_factory:
            user_service = service_factory.get_user_service()
            return await user_service.get_by_id(user_id)

    async def _update_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, user_id: int, user_dto: UserDTO
    ) -> None:
        async with service_factory:
            user_service = service_factory.get_user_service()
            await user_service.update_by_id(user_id, user_dto)

    async def _delete_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, user_id: int) -> None:
        async with service_factory:
            user_service = service_factory.get_user_service()
            await user_service.delete_by_id(user_id)

    async def _get_by_telegram_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, telegram_id: int
    ) -> UserModel:
        async with service_factory:
            user_service = service_factory.get_user_service()
            return await user_service.get_by_telegram_id(telegram_id)

    async def _delete_by_telegram_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, telegram_id: int
    ) -> None:
        async with service_factory:
            user_service = service_factory.get_user_service()
            await user_service.delete_by_telegram_id(telegram_id)

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[UserModel]:
        async with service_factory:
            user_service = service_factory.get_user_service()
            return await user_service.get_all_paginated()

    async def _get_by_subscription(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        users_by_subscription: USERS_BY_SUBSCIPTION_PARAMS = Query(None),
    ):
        async with service_factory:
            user_service = service_factory.get_user_service()
            return list(
                await user_service.get_users_by_subcription(
                    users_by_subscription.weapon_id,
                    users_by_subscription.skin_id,
                    users_by_subscription.quality_id,
                    users_by_subscription.stattrak,
                )
            )
