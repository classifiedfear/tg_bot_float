from typing import List

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_CREATED_MSG,
    ENTITY_DELETED_MSG,
    ENTITY_UPDATED_MSG,
)
from tg_bot_float_common_dtos.skin_dto import SkinDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY


class SkinRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/skins", tags=["skins"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/create", self._create, response_model=None, methods=["POST"])
        self._router.add_api_route(
            "/id/{skin_id}", self._get_skin_by_id, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/id/{skin_id}", self._update_skin_by_id, response_model=None, methods=["PUT"]
        )
        self._router.add_api_route("/id/{skin_id}", self._delete_skin_by_id, methods=["DELETE"])
        self._router.add_api_route(
            "/name/{skin_name}", self._get_skin_by_name, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/name/{skin_name}", self._update_skin_by_name, response_model=None, methods=["PUT"]
        )
        self._router.add_api_route(
            "/name/{skin_name}", self._delete_skin_by_name, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/create_many", self._create_many, response_model=None, methods=["POST"]
        )
        self._router.add_api_route("/", self._get_all, response_model=None, methods=["GET"])
        self._router.add_api_route("/id", self._delete_many_by_id, methods=["DELETE"])
        self._router.add_api_route("/name", self._delete_many_by_name, methods=["DELETE"])

    async def _create(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_dto: SkinDTO,
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.create(skin_dto)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Skin"),
                    "item": SkinDTO.model_validate(
                        skin_db_model,
                    ).model_dump(),
                },
            )

    async def _get_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.get_by_id(skin_id)
            return JSONResponse(
                content={
                    "item": SkinDTO.model_validate(
                        skin_db_model,
                    ).model_dump()
                }
            )

    async def _update_skin_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_id: int,
        skin_dto: SkinDTO,
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.update_by_id(skin_id, skin_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Skin"),
                    "item": SkinDTO.model_validate(
                        skin_db_model,
                    ).model_dump(),
                },
            )

    async def _delete_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_by_id(skin_id)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Skin", identifier="id", entity_identifier=str(skin_id)
                    )
                },
            )

    async def _get_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.get_by_name(skin_name)
            return JSONResponse(
                content={
                    "item": SkinDTO.model_validate(
                        skin_db_model,
                    ).model_dump()
                }
            )

    async def _update_skin_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_name: str,
        skin_dto: SkinDTO,
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.update_by_name(skin_name, skin_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Skin"),
                    "item": SkinDTO.model_validate(
                        skin_db_model,
                    ).model_dump(),
                }
            )

    async def _delete_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_by_name(skin_name)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Skin", identifier="name", entity_identifier=str(skin_name)
                    )
                }
            )

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_dtos: List[SkinDTO]
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_models = await skin_service.create_many(skin_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Qualities"),
                    "items": [
                        SkinDTO.model_validate(
                            skin_db_model,
                        ).model_dump()
                        for skin_db_model in skin_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_models = await skin_service.get_all()
            return JSONResponse(
                content={
                    "items": [
                        SkinDTO.model_validate(
                            skin_db_model,
                        ).model_dump()
                        for skin_db_model in skin_db_models
                    ]
                }
            )

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_many_by_id(ids)
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
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_many_by_name(names)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Qualities", identifier="names", entity_identifier=", ".join(names)
                    )
                }
            )
