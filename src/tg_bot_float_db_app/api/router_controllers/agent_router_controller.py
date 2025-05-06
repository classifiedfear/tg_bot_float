from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page

from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.agent_model import AgentModel
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController


class AgentRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/agents", tags=["agents"])
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
            "/id/{agent_id}", self._get_by_id, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/id/{agent_id}",
            self._update_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{agent_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{agent_name}",
            self._get_by_name,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/name/{agent_name}",
            self._update_by_name,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{agent_name}",
            self._delete_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[AgentDTO]
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
            "/id", self._get_many_by_id, methods=["GET"], response_model=Page[AgentDTO]
        )
        self._router.add_api_route(
            "/name", self._get_many_by_name, methods=["GET"], response_model=Page[AgentDTO]
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, agent_dto: AgentDTO
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            agent_db_model = await agent_service.create(agent_dto)
            response.headers["Location"] = f"/agents/id/{agent_db_model.id}"

    async def _get_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> AgentModel:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            return await agent_service.get_by_id(quality_id)

    async def _update_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, agent_id: int, agent_dto: AgentDTO
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.update_by_id(agent_id, agent_dto)

    async def _delete_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, agent_id: int) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.delete_by_id(agent_id)

    async def _get_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, agent_name: str
    ) -> AgentModel:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            return await agent_service.get_by_name(agent_name)

    async def _update_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        agent_name: str,
        agent_dto: AgentDTO,
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.update_by_name(agent_name, agent_dto)

    async def _delete_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, agent_name: str
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.delete_by_name(agent_name)

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, agent_dtos: List[AgentDTO]
    ) -> JSONResponse:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            agent_models = await agent_service.create_many(agent_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [f"/agents/id/{agent_model.id}" for agent_model in agent_models],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[AgentModel]:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            return await agent_service.get_all_paginated()

    async def _get_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> Page[AgentModel]:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            return await agent_service.get_many_by_id_paginated(ids)

    async def _get_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> Page[AgentModel]:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            return await agent_service.get_many_by_name_paginated(names)

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> None:
        async with service_factory:
            agent_service = service_factory.get_agent_service()
            await agent_service.delete_many_by_name(names)
