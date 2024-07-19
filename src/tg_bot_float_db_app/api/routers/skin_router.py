from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page


from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.skin_model import SkinModel


class SkinRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/skins", tags=["skins"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route(
            "/create",
            self._create,
            response_model=None,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/id/{skin_id}", self._get_skin_by_id, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/id/{skin_id}",
            self._update_skin_by_id,
            response_model=None,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{skin_id}",
            self._delete_skin_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{skin_name}", self._get_skin_by_name, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/name/{skin_name}",
            self._update_skin_by_name,
            response_model=None,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{skin_name}",
            self._delete_skin_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many",
            self._create_many,
            response_model=None,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/", self._get_all, response_model=Page[SkinDTO], methods=["GET"]
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

    async def _create(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        response: Response,
        skin_dto: SkinDTO,
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_model = await skin_service.create(skin_dto)
            response.headers["Location"] = f"/skins/id/{skin_db_model.id}"

    async def _get_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            return await skin_service.get_by_id(skin_id)

    async def _update_skin_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_id: int,
        skin_dto: SkinDTO,
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.update_by_id(skin_id, skin_dto)

    async def _delete_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_by_id(skin_id)

    async def _get_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            return await skin_service.get_by_name(skin_name)

    async def _update_skin_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_name: str,
        skin_dto: SkinDTO,
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.update_by_name(skin_name, skin_dto)

    async def _delete_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_by_name(skin_name)

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_dtos: List[SkinDTO]
    ) -> JSONResponse:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            skin_db_models = await skin_service.create_many(skin_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [f"/skins/id/{skin_db_model.id}" for skin_db_model in skin_db_models],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[SkinDTO]:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            return await skin_service.get_all_paginated()

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> None:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            await skin_service.delete_many_by_name(names)
