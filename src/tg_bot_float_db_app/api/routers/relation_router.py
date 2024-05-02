from typing import List

import fastapi
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import ITEM_EXIST_MSG, ITEM_NOT_EXIST_MSG, \
    ITEM_DELETED_MSG
from tg_bot_float_common_dtos.relation_id_dto import RelationIdDTO
from tg_bot_float_db_app.api.dependencies.service_factory import DbServiceFactory


RELATION_ROUTER = fastapi.APIRouter(prefix="/relations", tags=["relations"])



@RELATION_ROUTER.post('', response_model=None)
async def create(
    service_factory: DbServiceFactory, relation_id_dto: RelationIdDTO) -> MsgResponseDTO | RelationModel:
    relation_service = service_factory.get_relation_service()
    try:
        relation_model = await relation_service.create(relation_id_dto)
    except IntegrityError:
        return MsgResponseDTO(
            status=False, msg=ITEM_EXIST_MSG.format(
                item='Relation',
                identifier='ids',
                item_identifier=', '.join(
                    [
                        str(relation_id_dto.weapon_id),
                        str(relation_id_dto.skin_id),
                        str(relation_id_dto.quality_id)]
                    )
                )
            )
    return relation_model


@RELATION_ROUTER.get('{weapon_id}/{skin_id}/{quality_id}', response_model=None)
async def get_relation_by_id(
        service_factory: DbServiceFactory, weapon_id: int, skin_id: int, quality_id: int,
) -> MsgResponseDTO | RelationModel:
    relation_service = service_factory.get_relation_service()
    if relation_db_model := await relation_service.get_by_id(weapon_id, skin_id, quality_id):
        return relation_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(
            item='Relation',
            identifier='ids',
            item_identifier=', '.join([str(weapon_id), str(skin_id), str(quality_id)])
        ))


@RELATION_ROUTER.delete('{weapon_id}/{skin_id}/{quality_id}')
async def delete_relation_by_id(
        service_factory: DbServiceFactory, weapon_id: int, skin_id: int, quality_id: int,
) -> MsgResponseDTO:
    relation_service = service_factory.get_relation_service()
    try:
        await relation_service.delete_by_id(weapon_id, skin_id, quality_id)
    except BotDbDeleteException:
        return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(
            item='Relation',
            identifier='ids',
            item_identifier=', '.join([str(weapon_id), str(skin_id), str(quality_id)]))
        )

    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item="Relation",
            identifier='ids',
            item_identifier=', '.join(
                [str(weapon_id), str(skin_id), str(quality_id)]
                ))
        )

@RELATION_ROUTER.post("/create_many", response_model=None)
async def create_many(
    service_factory: DbServiceFactory, relation_id_dtos: List[RelationIdDTO],
    ) -> List[RelationModel] | MsgResponseDTO:
    relation_service = service_factory.get_relation_service()
    try:
        relation_db_models = await relation_service.create_many(relation_id_dtos)
    except IntegrityError:
        ids = [
            (relation_post_model.weapon_id, relation_post_model.skin_id, relation_post_model.quality_id)
            for relation_post_model in relation_id_dtos
            ]
        existence_quality_db_models = await relation_service.get_many_by_id(ids)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Relation',
                identifier='ids',
                item_names=', '.join(
                    f'({relation.weapon_id}, {relation.skin_id}, {relation.quality_id})'
                    for relation in existence_quality_db_models)
                )
            )
    return relation_db_models

@RELATION_ROUTER.get('', response_model=None)
async def get_relations(service_factory: DbServiceFactory) -> List[RelationModel]:
    relation_service = service_factory.get_relation_service()
    return list(await relation_service.get_all())
