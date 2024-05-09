from typing import List

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.misc.router_constants import (
    ENTITY_CREATED_MSG,
    ENTITY_DELETED_MSG,
    ENTITY_UPDATED_MSG,
)
from tg_bot_float_common_dtos.quality_dto import QualityDTO


class QualityRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/qualities", tags=["qualities"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/create", self._create, response_model=None, methods=["POST"])
        self._router.add_api_route("/id/{quality_id}", self._get_quality_by_id, methods=["GET"])
        self._router.add_api_route("/id/{quality_id}", self._update_quality_by_id, methods=["PUT"])
        self._router.add_api_route(
            "/id/{quality_id}", self._delete_quality_by_id, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/name/{quality_name}", self._get_quality_by_name, methods=["GET"]
        )
        self._router.add_api_route(
            "/name/{quality_name}",
            self._update_quality_by_name,
            methods=["PUT"],
        )
        self._router.add_api_route(
            "/name/{quality_name}", self._delete_quality_by_name, methods=["DELETE"]
        )
        self._router.add_api_route("/create_many", self._create_many, methods=["POST"])
        self._router.add_api_route("/", self._get_all, methods=["GET"])
        self._router.add_api_route("/id", self._delete_many_by_id, methods=["DELETE"])
        self._router.add_api_route("/name", self._delete_many_by_name, methods=["DELETE"])

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_dto: QualityDTO
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.create(quality_dto)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Quality"),
                    "item": QualityDTO.model_validate(
                        quality_db_model,
                    ).model_dump(),
                },
            )

    async def _get_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.get_by_id(quality_id)
            return JSONResponse(
                content={
                    "item": QualityDTO.model_validate(
                        quality_db_model,
                    ).model_dump()
                }
            )

    async def _update_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int, quality_dto: QualityDTO
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.update_by_id(quality_id, quality_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Quality"),
                    "item": QualityDTO.model_validate(
                        quality_db_model,
                    ).model_dump(),
                },
            )

    async def _delete_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_by_id(quality_id)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Quality", identifier="id", entity_identifier=str(quality_id)
                    )
                },
            )

    async def _get_quality_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.get_by_name(quality_name)
            return JSONResponse(
                content={
                    "item": QualityDTO.model_validate(
                        quality_db_model,
                    ).model_dump()
                }
            )

    async def _update_quality_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        quality_name: str,
        quality_dto: QualityDTO,
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_model = await quality_service.update_by_name(quality_name, quality_dto)
            return JSONResponse(
                content={
                    "message": ENTITY_UPDATED_MSG.format(entity="Quality"),
                    "item": QualityDTO.model_validate(
                        quality_db_model,
                    ).model_dump(),
                }
            )

    async def _delete_quality_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_by_name(quality_name)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Quality", identifier="name", entity_identifier=str(quality_name)
                    )
                }
            )

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_dtos: List[QualityDTO]
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_models = await quality_service.create_many(quality_dtos)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": ENTITY_CREATED_MSG.format(entity="Qualities"),
                    "items": [
                        QualityDTO.model_validate(
                            quality_db_model,
                        ).model_dump()
                        for quality_db_model in quality_db_models
                    ],
                },
            )

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            quality_db_models = await quality_service.get_all()
            return JSONResponse(
                content={
                    "items": [
                        QualityDTO.model_validate(
                            quality_db_model,
                        ).model_dump()
                        for quality_db_model in quality_db_models
                    ]
                }
            )

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> JSONResponse:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_many_by_id(ids)
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
            quality_service = service_factory.get_quality_service()
            await quality_service.delete_many_by_name(names)
            return JSONResponse(
                content={
                    "message": ENTITY_DELETED_MSG.format(
                        entity="Qualities", identifier="names", entity_identifier=", ".join(names)
                    )
                }
            )
