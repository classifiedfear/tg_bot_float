from typing import List

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination.links import Page

from tg_bot_float_common_dtos.schema_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.db_app_dtos.relation_name_dto import RelationNameDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.api.dependencies.params import RELATION_ID_REQUEST, RELATION_NAME_REQUEST
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)


class RelationRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/relations", tags=["relations"])
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/create", self._create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._get_by_id,
            methods=["GET"],
            response_model=None,
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._delete_by_id,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/create_many", self._create_many, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self._router.add_api_route(
            "", self._get_all, methods=["GET"], response_model=Page[RelationDTO]
        )
        self._router.add_api_route(
            "/names_by_id/{weapon_id}/{skin_id}/{quality_id}",
            self._get_weapon_skin_quality_name_by_id,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/ids_by_name/{weapon_name}/{skin_name}/{quality_name}",
            self._get_weapon_skin_quality_id_by_name,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/stattrak_existence/{weapon_id}/{skin_id}/{quality_id}",
            self._get_stattrak_existence,
            methods=["GET"],
        )

    async def _create(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        response: Response,
        relation_id_dto: RelationDTO,
    ) -> None:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_db_model = await relation_service.create(relation_id_dto)
            response.headers["Location"] = (
                f"/relations/{relation_db_model.weapon_id}/{relation_db_model.skin_id}/{relation_db_model.quality_id}/{relation_db_model.stattrak_existence}"
            )

    async def _get_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_request_dto: RELATION_ID_REQUEST = Query(),
    ) -> RelationModel:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_by_id(
                weapon_id=relation_id_request_dto.weapon_id,
                skin_id=relation_id_request_dto.skin_id,
                quality_id=relation_id_request_dto.quality_id,
            )

    async def _delete_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_request_dto: RELATION_ID_REQUEST = Query(),
    ) -> None:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            await relation_service.delete_by_id(
                weapon_id=relation_id_request_dto.weapon_id,
                skin_id=relation_id_request_dto.skin_id,
                quality_id=relation_id_request_dto.quality_id,
            )

    async def _create_many(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_dtos: List[RelationDTO],
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
                            f"/{relation_db_model.stattrak_existence}"
                        )
                        for relation_db_model in relation_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> Page[RelationModel]:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_all_paginated()

    async def _get_weapon_skin_quality_name_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_request_dto: RELATION_ID_REQUEST = Query(),
    ) -> RelationNameDTO:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_weapon_skin_quality_name_by_id(
                weapon_id=relation_id_request_dto.weapon_id,
                skin_id=relation_id_request_dto.skin_id,
                quality_id=relation_id_request_dto.quality_id,
            )

    async def _get_weapon_skin_quality_id_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_name_request_dto: RELATION_NAME_REQUEST = Query(),
    ) -> RelationDTO:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_weapon_skin_quality_id_by_name(
                weapon_name=relation_name_request_dto.weapon_name,
                skin_name=relation_name_request_dto.skin_name,
                quality_name=relation_name_request_dto.quality_name,
            )

    async def _get_stattrak_existence(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_request_dto: RELATION_ID_REQUEST = Query(),
    ) -> bool:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return await relation_service.get_stattrak_existence(
                weapon_id=relation_id_request_dto.weapon_id,
                skin_id=relation_id_request_dto.skin_id,
                quality_id=relation_id_request_dto.quality_id,
            )
