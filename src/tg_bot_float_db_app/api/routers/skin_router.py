from typing import List

from fastapi import APIRouter, Query
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import (
    ITEM_DELETED_MSG,
    ITEM_EXIST_MSG,
    ITEM_NOT_EXIST_MSG,
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
    ) -> MsgResponseDTO | SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                skin_db_model = await skin_service.create(skin_dto)
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Skin", identifier="name", item_identifier=skin_dto.name
                    ),
                )
            return skin_db_model

    async def _get_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> MsgResponseDTO | SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            if skin_db_model := await skin_service.get_by_id(skin_id):
                return skin_db_model
            return MsgResponseDTO(
                status=False,
                msg=ITEM_NOT_EXIST_MSG.format(
                    item="Skin", identifier="id", item_identifier=str(skin_id)
                ),
            )

    async def _update_skin_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_id: int,
        skin_dto: SkinDTO,
    ) -> MsgResponseDTO | SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                if (skin_db_model := await skin_service.update_by_id(skin_id, skin_dto)) is None:
                    return MsgResponseDTO(
                        status=False,
                        msg=ITEM_NOT_EXIST_MSG.format(
                            item="Skin", identifier="id", item_identifier=str(skin_id)
                        ),
                    )
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Skin", identifier="name", item_name=skin_dto.name
                    ),
                )
            return skin_db_model

    async def _delete_skin_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_id: int
    ) -> MsgResponseDTO:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                await skin_service.delete_by_id(skin_id)
            except BotDbDeleteException:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Skin", identifier="id", item_identifier=str(skin_id)
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Skin", identifier="id", item_identifier=str(skin_id)
                ),
            )

    async def _get_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> MsgResponseDTO | SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            if skin_db_model := await skin_service.get_by_name(skin_name):
                return skin_db_model
            return MsgResponseDTO(
                status=False,
                msg=ITEM_NOT_EXIST_MSG.format(
                    item="Skin", identifier="name", item_identifier=skin_name
                ),
            )

    async def _update_skin_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        skin_name: str,
        skin_dto: SkinDTO,
    ) -> MsgResponseDTO | SkinModel:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                if (
                    skin_db_model := await skin_service.update_by_name(skin_name, skin_dto)
                ) is None:
                    return MsgResponseDTO(
                        status=False,
                        msg=ITEM_NOT_EXIST_MSG.format(
                            item="Skin", identifier="name", item_indeficator=skin_name
                        ),
                    )
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Skin", identifier="name", item_identifier=skin_name
                    ),
                )
            return skin_db_model

    async def _delete_skin_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, skin_name: str
    ) -> MsgResponseDTO:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                await skin_service.delete_by_name(skin_name)
            except BotDbDeleteException:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Skin", identifier="name", item_identifier=skin_name
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Skin", identifier="name", item_identifier=skin_name
                ),
            )

    async def _create_many(self, service_factory: BOT_DB_SERVICE_FACTORY, skin_dtos: List[SkinDTO]):
        skin_service = service_factory.get_skin_service()
        try:
            skin_db_models = await skin_service.create_many(skin_dtos)
        except IntegrityError:
            names = [skin_dto.name for skin_dto in skin_dtos if skin_dto.name]
            existence_skin_db_models = await skin_service.get_many_by_name(names)
            return MsgResponseDTO(
                status=False,
                msg=ITEM_EXIST_MSG.format(
                    item="Skin",
                    identifier="names",
                    item_identifier=",".join(skin.name for skin in existence_skin_db_models),
                ),
            )
        return skin_db_models

    async def _get_all(
        self, service_factory: BOT_DB_SERVICE_FACTORY
    ) -> MsgResponseDTO | List[SkinModel]:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            return list(await skin_service.get_all())

    async def _delete_many_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, ids: List[int] = Query(None)
    ) -> MsgResponseDTO:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                await skin_service.delete_many_by_id(ids)
            except BotDbDeleteException:
                existence_skin_db_models = await skin_service.get_many_by_id(ids)
                existence_ids = {skin.id for skin in existence_skin_db_models}
                difference_ids = set(ids).symmetric_difference(existence_ids)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Skin",
                        identifier="ids",
                        item_identifier=", ".join(str(id) for id in difference_ids),
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Skin", identifier="ids", item_identifier=", ".join(str(id) for id in ids)
                ),
            )

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
    ) -> MsgResponseDTO:
        async with service_factory:
            skin_service = service_factory.get_skin_service()
            try:
                await skin_service.delete_many_by_name(names)
            except BotDbDeleteException:
                existence_skin_db_models = await skin_service.get_many_by_name(names)
                existence_names = {skin.name for skin in existence_skin_db_models}
                difference_names = set(names).symmetric_difference(existence_names)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Skin",
                        identifier="names",
                        item_identifier=", ".join(name for name in difference_names),
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Skin", identifier="names", item_identifier=", ".join(names)
                ),
            )
