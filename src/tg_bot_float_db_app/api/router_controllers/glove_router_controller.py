from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page

from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.glove_model import GloveModel
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController


class GloveRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/gloves", tags=["gloves"])
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/create",
            self._create,
            response_model=None,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/id/{glove_id}", self._get_by_id, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/id/{glove_id}",
            self._update_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{glove_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{glove_name}",
            self._get_by_name,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/name/{glove_name}",
            self._update_by_name,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{glove_name}",
            self._delete_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[GloveDTO]
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
            "/id", self._get_many_by_id, methods=["GET"], response_model=Page[GloveDTO]
        )
        self._router.add_api_route(
            "/name", self._get_many_by_name, methods=["GET"], response_model=Page[GloveDTO]
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, glove_dto: GloveDTO
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            agent_db_model = await glove_service.create(glove_dto)
            response.headers["Location"] = f"/gloves/id/{agent_db_model.id}"

    async def _get_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> GloveModel:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            return await glove_service.get_by_id(quality_id)

    async def _update_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, glove_id: int, glove_dto: GloveDTO
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.update_by_id(glove_id, glove_dto)

    async def _delete_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, glove_id: int) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.delete_by_id(glove_id)

    async def _get_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, glove_name: str
    ) -> GloveModel:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            return await glove_service.get_by_name(glove_name)

    async def _update_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        glove_name: str,
        glove_dto: GloveDTO,
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.update_by_name(glove_name, glove_dto)

    async def _delete_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, glove_name: str
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.delete_by_name(glove_name)

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, glove_dtos: List[GloveDTO]
    ) -> JSONResponse:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            agent_models = await glove_service.create_many(glove_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [f"/agents/id/{agent_model.id}" for agent_model in agent_models],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[GloveModel]:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            return await glove_service.get_all_paginated()

    async def _get_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> Page[GloveModel]:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            return await glove_service.get_many_by_id_paginated(ids)

    async def _get_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> Page[GloveModel]:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            return await glove_service.get_many_by_name_paginated(names)

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> None:
        async with service_factory:
            glove_service = service_factory.get_glove_service()
            await glove_service.delete_many_by_name(names)
