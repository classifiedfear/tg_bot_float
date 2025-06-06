from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO


class QualityRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/qualities", tags=["qualities"])
        super().__init__()

    def _init_routes(self):
        self._router.add_api_route(
            "/create",
            self._create,
            response_model=None,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/id/{quality_id}", self._get_by_id, methods=["GET"], response_model=None
        )
        self._router.add_api_route(
            "/id/{quality_id}",
            self._update_by_id,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/id/{quality_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{quality_name}",
            self._get_by_name,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "/name/{quality_name}",
            self._update_by_name,
            methods=["PUT"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/name/{quality_name}",
            self._delete_by_name,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "/", self._get_all, methods=["GET"], response_model=Page[QualityDTO]
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
            "/name/{weapon_name}/{skin_name}",
            self._get_many_by_weapon_skin_name,
            methods=["GET"],
            response_model=Page[QualityDTO],
        )
        self._router.add_api_route(
            "/id/{weapon_id}/{skin_id}",
            self._get_many_by_weapon_skin_id,
            methods=["GET"],
            response_model=Page[QualityDTO],
        )
        self._router.add_api_route(
            "/id", self._get_many_by_id, methods=["GET"], response_model=Page[QualityDTO]
        )
        self._router.add_api_route(
            "/name", self._get_many_by_name, methods=["GET"], response_model=Page[QualityDTO]
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, response: Response, quality_dto: QualityDTO
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.create(quality_dto)
            response.headers["Location"] = f"/qualities/id/{quality_db_model.id}"

    async def _get_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_by_id(quality_id)

    async def _update_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int, quality_dto: QualityDTO
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.update_by_id(quality_id, quality_dto)

    async def _delete_by_id(self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_by_id(quality_id)

    async def _get_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_by_name(quality_name)

    async def _update_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        quality_name: str,
        quality_dto: QualityDTO,
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.update_by_name(quality_name, quality_dto)

    async def _delete_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_by_name(quality_name)

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_dtos: List[QualityDTO]
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_models = await quality_service.create_many(quality_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [
                        f"/qualities/id/{quality_db_model.id}"
                        for quality_db_model in quality_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_all_paginated()

    async def _get_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> Page[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_many_by_id_paginated(ids)

    async def _get_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> Page[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_many_by_name_paginated(names)

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query()
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_many_by_id(ids)

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query()
    ) -> None:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_many_by_name(names)

    async def _get_many_by_weapon_skin_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str, skin_name: str
    ) -> Page[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_many_by_weapon_skin_name_paginated(
                weapon_name, skin_name
            )

    async def _get_many_by_weapon_skin_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int, skin_id: int
    ) -> Page[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            return await quality_service.get_many_by_weapon_skin_id_paginated(weapon_id, skin_id)
