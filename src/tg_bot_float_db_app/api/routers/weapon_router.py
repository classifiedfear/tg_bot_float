from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse


from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class WeaponRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/weapons", tags=["weapons"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/id/{weapon_id}", self._get_weapon_by_id, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/id/{weapon_id}",
            self._update_weapon_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{weapon_id}",
            self._delete_weapon_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._get_weapon_by_name, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/name/{weapon_name}",
            self._update_weapon_by_name,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{weapon_name}",
            self._delete_weapon_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route("/", self._get_all, methods=["GET"], response_model=None)
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

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.create(weapon_dto)
            response.headers["Location"] = f"/weapons/id/{weapon_db_model.id}"

    async def _get_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
    ) -> WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_by_id(weapon_id)

    async def _update_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.update_by_id(weapon_id, weapon_dto)

    async def _delete_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_by_id(weapon_id)

    async def _get_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
    ) -> WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return await weapon_service.get_by_name(weapon_name)

    async def _update_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str, weapon_dto: WeaponDTO
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.update_by_name(weapon_name, weapon_dto)

    async def _delete_weapon_by_name(
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
                        f"/weapons/id/{weapon_db_model.id}"
                        for weapon_db_model in weapon_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> List[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return list(await weapon_service.get_all())

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> None:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_name(names)
