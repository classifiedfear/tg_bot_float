from typing import List

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_common_dtos.schema_dtos.relation_id_dto import RelationIdDTO


class RelationRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/relations", tags=["relations"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._get_relation_by_id,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._delete_relation_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "", self._get_all, methods=["GET"], response_model=Page[RelationIdDTO]
        )

    async def _create(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        response: Response,
        relation_id_dto: RelationIdDTO,
    ) -> None:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_db_model = await relation_service.create(relation_id_dto)
            response.headers["Location"] = (
                f"/relations/{relation_db_model.weapon_id}/{relation_db_model.skin_id}/{relation_db_model.quality_id}"
            )

    async def _get_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> RelationModel:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_by_id(weapon_id, skin_id, quality_id)

    async def _delete_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> None:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            await relation_service.delete_by_id(weapon_id, skin_id, quality_id)

    async def _create_many(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_dtos: List[RelationIdDTO],
    ) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_db_models = await relation_service.create_many(relation_id_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "items": [
                        (
                            f"/relations/{relation_db_model.weapon_id}"
                            f"/{relation_db_model.skin_id}"
                            f"/{relation_db_model.quality_id}"
                        )
                        for relation_db_model in relation_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[RelationIdDTO]:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_all()
