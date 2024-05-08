from typing import List

from fastapi import APIRouter, Query
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import (
    ITEM_EXIST_MSG,
    ITEM_NOT_EXIST_MSG,
    ITEM_DELETED_MSG,
)
from tg_bot_float_common_dtos.quality_dto import QualityDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY


class QualityRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/qualities", tags=["qualities"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/create", self._create, response_model=None, methods=["POST"])
        self._router.add_api_route(
            "/id/{quality_id}", self._get_quality_by_id, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/id/{quality_id}", self._update_quality_by_id, response_model=None, methods=["PUT"]
        )
        self._router.add_api_route(
            "/id/{quality_id}", self._delete_quality_by_id, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/name/{quality_name}", self._get_quality_by_name, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/name/{quality_name}",
            self._update_quality_by_name,
            response_model=None,
            methods=["PUT"],
        )
        self._router.add_api_route(
            "/name/{quality_name}", self._delete_quality_by_name, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/create_many", self._create_many, response_model=None, methods=["POST"]
        )
        self._router.add_api_route("/", self._get_all, response_model=None, methods=["GET"])
        self._router.add_api_route("/id", self._delete_many_by_id, methods=["DELETE"])
        self._router.add_api_route("/name", self._delete_many_by_name, methods=["DELETE"])

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_dto: QualityDTO
    ) -> MsgResponseDTO | QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                quality_db_model = await quality_service.create(quality_dto)
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Quality", identifier="name", item_identifier=quality_dto.name
                    ),
                )
            return quality_db_model

    async def _get_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> MsgResponseDTO | QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            if quality_db_model := await quality_service.get_by_id(quality_id):
                return quality_db_model
            return MsgResponseDTO(
                status=False,
                msg=ITEM_NOT_EXIST_MSG.format(
                    item="Quality", identifier="id", item_identifier=str(quality_id)
                ),
            )

    async def _update_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int, quality_dto: QualityDTO
    ) -> MsgResponseDTO | QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                if (
                    quality_db_model := await quality_service.update_by_id(quality_id, quality_dto)
                ) is None:
                    return MsgResponseDTO(
                        status=False,
                        msg=ITEM_NOT_EXIST_MSG.format(
                            item="Quality", identifier="id", item_identifier=str(quality_id)
                        ),
                    )
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Quality", identifier="name", item_name=quality_dto.name
                    ),
                )
            return quality_db_model

    async def _delete_quality_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_id: int
    ) -> MsgResponseDTO:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                await quality_service.delete_by_id(quality_id)
            except BotDbDeleteException:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Quality", identifier="id", item_identifier=str(quality_id)
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Quality", identifier="id", item_identifier=str(quality_id)
                ),
            )

    async def _get_quality_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> MsgResponseDTO | QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            if quality_db_model := await quality_service.get_by_name(quality_name):
                return quality_db_model
            return MsgResponseDTO(
                status=False,
                msg=ITEM_NOT_EXIST_MSG.format(
                    item="Quality", identifier="name", item_identifier=quality_name
                ),
            )

    async def _update_quality_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        quality_name: str,
        quality_dto: QualityDTO,
    ) -> MsgResponseDTO | QualityModel:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                if (
                    quality_db_model := await quality_service.update_by_name(
                        quality_name, quality_dto
                    )
                ) is None:
                    return MsgResponseDTO(
                        status=False,
                        msg=ITEM_NOT_EXIST_MSG.format(
                            item="Quality", identifier="name", item_identifier=quality_name
                        ),
                    )
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Quality", identifier="name", item_identifier=quality_dto.name
                    ),
                )
            return quality_db_model

    async def _delete_quality_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_name: str
    ) -> MsgResponseDTO:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                await quality_service.delete_by_name(quality_name)
            except BotDbDeleteException:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Quality", identifier="name", item_identifier=quality_name
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Quality", identifier="name", item_identifier=quality_name
                ),
            )

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, quality_dtos: List[QualityDTO]
    ) -> MsgResponseDTO | List[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                quality_db_models = await quality_service.create_many(quality_dtos)
            except IntegrityError:
                names = [quality_dto.name for quality_dto in quality_dtos if quality_dto.name]
                existence_quality_db_models = await quality_service.get_many_by_name(names)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Quality",
                        identifier="names",
                        item_identifier=",".join(
                            quality.name for quality in existence_quality_db_models
                        ),
                    ),
                )
            return quality_db_models

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> List[QualityModel]:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
        return list(await quality_service.get_all())

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> MsgResponseDTO:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                await quality_service.delete_many_by_id(ids)
            except BotDbDeleteException:
                existence_quality_db_models = await quality_service.get_many_by_id(ids)
                existence_ids = {quality.id for quality in existence_quality_db_models}
                difference_ids = set(ids).symmetric_difference(existence_ids)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Quality",
                        identifier="ids",
                        item_identifier=", ".join(str(id) for id in difference_ids),
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Quality",
                    identifier="ids",
                    item_identifier=", ".join(str(id) for id in ids),
                ),
            )

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> MsgResponseDTO:
        async with service_factory:
            quality_service = service_factory.get_quality_service()
            try:
                await quality_service.delete_many_by_name(names)
            except BotDbDeleteException:
                existence_quality_db_models = await quality_service.get_many_by_name(names)
                existence_names = {quality.name for quality in existence_quality_db_models}
                difference_names = set(names).symmetric_difference(existence_names)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Quality",
                        identifier="names",
                        item_identifier=", ".join(name for name in difference_names),
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Quality", identifier="names", item_identifier=", ".join(names)
                ),
            )
