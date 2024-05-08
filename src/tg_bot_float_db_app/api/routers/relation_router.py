from typing import List

from fastapi import APIRouter, Query
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import (
    ITEM_EXIST_MSG,
    ITEM_NOT_EXIST_MSG,
    ITEM_DELETED_MSG,
)
from tg_bot_float_common_dtos.relation_id_dto import RelationIdDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY


class RelationRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/relations", tags=["relations"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/create", self._create, response_model=None, methods=["POST"])
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}",
            self._get_relation_by_id,
            response_model=None,
            methods=["GET"],
        )
        self._router.add_api_route(
            "{weapon_id}/{skin_id}/{quality_id}", self._delete_relation_by_id, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/create_many", self._create_many, response_model=None, methods=["POST"]
        )
        self._router.add_api_route("", self._get_all, response_model=None, methods=["GET"])
        self._router.add_api_route(
            "/skins/name/", self._get_filtered_by_name_skins, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/skins/id/", self._get_filtered_by_id_skins, response_model=None, methods=["GET"]
        )

    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, relation_id_dto: RelationIdDTO
    ) -> MsgResponseDTO | RelationModel:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            try:
                relation_model = await relation_service.create(relation_id_dto)
            except IntegrityError:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Relation",
                        identifier="ids",
                        item_identifier=", ".join(
                            [
                                str(relation_id_dto.weapon_id),
                                str(relation_id_dto.skin_id),
                                str(relation_id_dto.quality_id),
                            ]
                        ),
                    ),
                )
            return relation_model

    async def _get_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> MsgResponseDTO | RelationModel:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            if relation_db_model := await relation_service.get_by_id(
                weapon_id, skin_id, quality_id
            ):
                return relation_db_model
            return MsgResponseDTO(
                status=False,
                msg=ITEM_NOT_EXIST_MSG.format(
                    item="Relation",
                    identifier="ids",
                    item_identifier=", ".join([str(weapon_id), str(skin_id), str(quality_id)]),
                ),
            )

    async def _delete_relation_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        skin_id: int,
        quality_id: int,
    ) -> MsgResponseDTO:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            try:
                await relation_service.delete_by_id(weapon_id, skin_id, quality_id)
            except BotDbDeleteException:
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(
                        item="Relation",
                        identifier="ids",
                        item_identifier=", ".join([str(weapon_id), str(skin_id), str(quality_id)]),
                    ),
                )
            return MsgResponseDTO(
                status=True,
                msg=ITEM_DELETED_MSG.format(
                    item="Relation",
                    identifier="ids",
                    item_identifier=", ".join([str(weapon_id), str(skin_id), str(quality_id)]),
                ),
            )

    async def _create_many(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        relation_id_dtos: List[RelationIdDTO],
    ) -> List[RelationModel] | MsgResponseDTO:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            try:
                relation_db_models = await relation_service.create_many(relation_id_dtos)
            except IntegrityError:
                ids = [
                    (
                        relation_post_model.weapon_id,
                        relation_post_model.skin_id,
                        relation_post_model.quality_id,
                    )
                    for relation_post_model in relation_id_dtos
                ]
                existence_quality_db_models = await relation_service.get_many_by_id(ids)
                return MsgResponseDTO(
                    status=False,
                    msg=ITEM_EXIST_MSG.format(
                        item="Relation",
                        identifier="weapon_id, skin_id, quality_id",
                        item_names=", ".join(
                            f"({relation.weapon_id}, {relation.skin_id}, {relation.quality_id})"
                            for relation in existence_quality_db_models
                        ),
                    ),
                )
            return relation_db_models

    async def _get_all(self, service_factory: BOT_DB_SERVICE_FACTORY) -> List[RelationModel]:
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return list(await relation_service.get_all())

    async def _get_filtered_by_name_skins(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon: str | None = None,
        quality: str | None = None,
        stattrak_existence: bool | None = None,
    ):
        async with service_factory:
            relation_service = service_factory.get_relation_service()
            return set(
                await relation_service.get_skins_by_name_for(
                    weapon_name=weapon, quality_name=quality, stattrak_existence=stattrak_existence
                )
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
            return set(
                await relation_service.get_skins_by_id_for(
                    weapon_id=weapon, quality_id=quality, stattrak_existence=stattrak_existence
                )
            )
