from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page


from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class WeaponRouterController(AbstractRouterController):
    def __init__(self):
        self._router = APIRouter(prefix="/weapons", tags=["weapons"])
        super().__init__()

    def _init_routes(self):
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/id/{weapon_id}", self._get_by_id, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/id/{weapon_id}",
            self._update_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{weapon_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._get_by_name, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/name/{weapon_name}",
            self._update_by_name,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{weapon_name}",
            self._delete_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[WeaponDTO]
        )
        self._router.add_api_route(
            "/id",
            self._delete_many_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name",
            self._delete_many_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id", self._get_many_by_id, methods=["GET"], response_model=Page[WeaponDTO]
        )
        self._router.add_api_route(
            "/name", self._get_many_by_name, methods=["GET"], response_model=Page[WeaponDTO]
        )
        self._router.add_api_route(
            "/skin/id/{skin_id}",
            self._get_many_by_skin_name,
            methods=["GET"],
            response_model=Page[WeaponDTO],
        )
        self._router.add_api_route(
            "/skin/name/{skin_name}",
            self._get_many_by_skin_name,
            methods=["GET"],
            response_model=Page[WeaponDTO],
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.create(weapon_dto)
            response.headers["Location"] = f"/weapons/id/{weapon_db_model.id}"

    async def _get_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
    ) -> WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_by_id(weapon_id)

    async def _update_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.update_by_id(weapon_id, weapon_dto)

    async def _delete_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_by_id(weapon_id)

    async def _get_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
    ) -> WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_by_name(weapon_name)

    async def _update_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.update_by_name(weapon_name, weapon_dto)

    async def _delete_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_by_name(weapon_name)

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_dtos: List[WeaponDTO]
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_models = await weapon_service.create_many(weapon_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [
                        f"/weapons/id/{weapon_db_model.id}" for weapon_db_model in weapon_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_all_paginated()

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_name(names)

    async def _get_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> Page[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_many_by_id_paginated(ids)

    async def _get_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> Page[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_many_by_name_paginated(names)

    async def _get_many_by_skin_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> Page[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_many_by_skin_name_paginated(skin_name)

    async def _get_many_by_skin_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> Page[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_many_by_skin_id_paginated(skin_id)
