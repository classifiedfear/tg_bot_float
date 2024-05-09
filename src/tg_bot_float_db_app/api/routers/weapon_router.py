from typing import List

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse


from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_CREATED_MSG,
    ENTITY_DELETED_MSG,
    ENTITY_UPDATED_MSG,
)
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO


class WeaponRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/weapons", tags=["weapons"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/create", self._create, methods=["POST"])
        self._router.add_api_route("/id/{weapon_id}", self._get_weapon_by_id, methods=["GET"])
        self._router.add_api_route("/id/{weapon_id}", self._update_weapon_by_id, methods=["PUT"])
        self._router.add_api_route("/id/{weapon_id}", self._delete_weapon_by_id, methods=["DELETE"])
        self._router.add_api_route("/name/{weapon_name}", self._get_weapon_by_name, methods=["GET"])
        self._router.add_api_route(
            "/name/{weapon_name}", self._update_weapon_by_name, methods=["PUT"]
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._delete_weapon_by_name, methods=["DELETE"]
        )
        self._router.add_api_route("/create_many", self._create_many, methods=["POST"])
        self._router.add_api_route("/", self._get_all, methods=["GET"])
        self._router.add_api_route("/id", self._delete_many_by_id, methods=["DELETE"])
        self._router.add_api_route("/name", self._delete_many_by_name, methods=["DELETE"])

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_dto: WeaponDTO
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.create(weapon_dto)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Weapon"),
                    "item": WeaponDTO.model_validate(
                        weapon_db_model,
                    ).model_dump(),
                },
            )

    async def _get_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.get_by_id(weapon_id)
            return JSONResponse(
                content={
                    "item": WeaponDTO.model_validate(
                        weapon_db_model,
                    ).model_dump()
                }
            )

    async def _update_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int, weapon_dto: WeaponDTO
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.update_by_id(weapon_id, weapon_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Weapon"),
                    "item": WeaponDTO.model_validate(
                        weapon_db_model,
                    ).model_dump(),
                },
            )

    async def _delete_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_by_id(weapon_id)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Weapon", identifier="id", entity_identifier=str(weapon_id)
                    )
                },
            )

    async def _get_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.get_by_name(weapon_name)
            return JSONResponse(
                content={
                    "item": WeaponDTO.model_validate(
                        weapon_db_model,
                    ).model_dump()
                }
            )

    async def _update_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str, weapon_dto: WeaponDTO
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_model = await weapon_service.update_by_name(weapon_name, weapon_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Weapon"),
                    "item": WeaponDTO.model_validate(
                        weapon_db_model,
                    ).model_dump(),
                }
            )

    async def _delete_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_by_name(weapon_name)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Weapon", identifier="name", entity_identifier=str(weapon_name)
                    )
                }
            )

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_dtos: List[WeaponDTO]
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_models = await weapon_service.create_many(weapon_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Qualities"),
                    "items": [
                        WeaponDTO.model_validate(
                            weapon_db_model,
                        ).model_dump()
                        for weapon_db_model in weapon_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            weapon_db_models = await weapon_service.get_all()
            return JSONResponse(
                content={
                    "items": [
                        WeaponDTO.model_validate(
                            weapon_db_model,
                        ).model_dump()
                        for weapon_db_model in weapon_db_models
                    ]
                }
            )

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_id(ids)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Qualities",
                        identifier="ids",
                        entity_identifier=", ".join(str(id) for id in ids),
                    )
                }
            )

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            await weapon_service.delete_many_by_name(names)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Qualities", identifier="names", entity_identifier=", ".join(names)
                    )
                }
            )
