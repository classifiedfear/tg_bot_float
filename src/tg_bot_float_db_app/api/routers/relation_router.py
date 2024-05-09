from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_DELETED_MSG,
    ENTITY_CREATED_MSG,
)
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_common_dtos.relation_id_dto import RelationIdDTO


class RelationRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/relations", tags=["relations"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/create", self._create, methods=["POST"])
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._get_relation_by_id,
            methods=["GET"],
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}", self._delete_relation_by_id, methods=["DELETE"]
        )
        self._router.add_api_route("/create_many", self._create_many, methods=["POST"])
        self._router.add_api_route("", self._get_all, methods=["GET"])
        self._router.add_api_route(
            "/skins/name/", self._get_filtered_by_name_skins, methods=["GET"]
        )
        self._router.add_api_route("/skins/id/", self._get_filtered_by_id_skins, methods=["GET"])

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, relation_id_dto: RelationIdDTO
    ) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_model = await relation_service.create(relation_id_dto)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Relation"),
                    "item": RelationIdDTO.model_validate(
                        relation_model,
                    ).model_dump(),
                },
            )

    async def _get_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_db_model = await relation_service.get_by_id(weapon_id, skin_id, quality_id)
            return JSONResponse(
                content={"item": RelationIdDTO.model_validate(relation_db_model).model_dump()}
            )

    async def _delete_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            await relation_service.delete_by_id(weapon_id, skin_id, quality_id)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        item="Relation",
                        identifier="weapon_id, skin_id, quality_id",
                        item_identifier=f"({weapon_id}, {skin_id}, {quality_id})",
                    )
                }
            )

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
                    "message": ENTITY_CREATED_MSG.format(entity="Relations"),
                    "items": [
                        RelationIdDTO.model_validate(
                            relation_db_model,
                        ).model_dump()
                        for relation_db_model in relation_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            relation_db_models = await relation_service.get_all()
            return JSONResponse(
                content={
                    "items": [
                        RelationIdDTO.model_validate(
                            relation_db_model,
                        ).model_dump()
                        for relation_db_model in list(relation_db_models)
                    ]
                }
            )

    async def _get_filtered_by_name_skins(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon: str | None = None,
        quality: str | None = None,
        stattrak_existence: bool | None = None,
    ) -> JSONResponse:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            filtered_skins = await relation_service.get_skins_by_name_for(
                weapon_name=weapon, quality_name=quality, stattrak_existence=stattrak_existence
            )
            return JSONResponse(
                content={
                    "items": [
                        RelationIdDTO.model_validate(
                            skin_db_model,
                        ).model_dump()
                        for skin_db_model in list(filtered_skins)
                    ]
                }
            )

    async def _get_filtered_by_id_skins(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon: int | None = None,
        quality: int | None = None,
        stattrak_existence: bool | None = None,
    ):
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            filtered_skins = await relation_service.get_skins_by_id_for(
                weapon_id=weapon, quality_id=quality, stattrak_existence=stattrak_existence
            )
            return JSONResponse(
                content={
                    "items": [
                        RelationIdDTO.model_validate(
                            skin_db_model,
                        ).model_dump()
                        for skin_db_model in list(filtered_skins)
                    ]
                }
            )
