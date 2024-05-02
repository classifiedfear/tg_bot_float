from typing import List

import fastapi
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import ITEM_DELETED_MSG, ITEM_EXIST_MSG, \
    ITEM_NOT_EXIST_MSG
from tg_bot_float_common_dtos.skin_dto import SkinDTO
from tg_bot_float_db_app.api.dependencies.service_factory import DbServiceFactory

SKIN_ROUTER = fastapi.APIRouter(prefix="/skins", tags=["skins"])


@SKIN_ROUTER.post("/create", response_model=None)
async def create(
        service_factory: DbServiceFactory, skin_dto: SkinDTO,
) -> MsgResponseDTO | SkinModel:
    skin_service = service_factory.get_skin_service()
    try:
        skin_db_model = await skin_service.create(skin_dto)
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Skin', identifier='name', item_identifier=skin_dto.name)
            )
    return skin_db_model


@SKIN_ROUTER.get("/id/{skin_id}", response_model=None)
async def get_skin_by_id(
        service_factory: DbServiceFactory, skin_id: int
) -> MsgResponseDTO | SkinModel:
    skin_service = service_factory.get_skin_service()
    if skin_db_model := await skin_service.get_by_id(skin_id):
        return skin_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(item='Skin', identifier='id', item_identifier=str(skin_id))
        )


@SKIN_ROUTER.put("/id/{skin_id}", response_model=None)
async def update_skin_by_id(
        service_factory: DbServiceFactory, skin_id: int, skin_dto: SkinDTO,
) -> MsgResponseDTO | SkinModel:
    skin_service = service_factory.get_skin_service()
    try:
        if (skin_db_model := await skin_service.update_by_id(skin_id, skin_dto)) is None:
            return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Skin',
                identifier='id',
                item_identifier=str(skin_id))
            )
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Skin',
                identifier='name',
                item_name=skin_dto.name)
            )
    return skin_db_model


@SKIN_ROUTER.delete("/id/{skin_id}")
async def delete_skin_by_id(
        service_factory: DbServiceFactory, skin_id: int
) -> MsgResponseDTO:
    skin_service = service_factory.get_skin_service()
    try:
        await skin_service.delete_by_id(skin_id)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Skin',
                identifier='id',
                item_identifier=str(skin_id))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item="Skin",
            identifier='id',
            item_identifier=str(skin_id))
        )


@SKIN_ROUTER.get('/name/{skin_name}', response_model=None)
async def get_skin_by_name(
        service_factory: DbServiceFactory, skin_name: str
) -> MsgResponseDTO | SkinModel:
    skin_service = service_factory.get_skin_service()
    if skin_db_model := await skin_service.get_by_name(skin_name):
        return skin_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(item='Skin', identifier='name', item_identifier=skin_name)
        )


@SKIN_ROUTER.put('/name/{skin_name}', response_model=None)
async def update_skin_by_name(
        service_factory: DbServiceFactory, skin_name: str, skin_dto: SkinDTO,
):
    skin_service = service_factory.get_skin_service()
    try:
        if (skin_db_model := await skin_service.update_by_name(skin_name, skin_dto)) is None:
            return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(item='Skin', identifier='name', item_indeficator=skin_name))
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Skin', identifier='name', itet_identifier=skin_name)
            )
    return skin_db_model

@SKIN_ROUTER.delete('/name/{skin_name}')
async def delete_skin_by_name(
        service_factory: DbServiceFactory, skin_name: str
):
    skin_service = service_factory.get_skin_service()
    try:
        await skin_service.delete_by_name(skin_name)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Skin', identifier='name', item_identifier=skin_name)
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item="Skin", identifier='name', item_identifier=skin_name)
            )


@SKIN_ROUTER.post('/create_many', response_model=None)
async def create_many(
        service_factory: DbServiceFactory, skin_dtos: List[SkinDTO]
):
    skin_service = service_factory.get_skin_service()
    try:
        skin_db_models = await skin_service.create_many(skin_dtos)
    except IntegrityError:
        names = [skin_dto.name for skin_dto in skin_dtos]
        existence_skin_db_models = await skin_service.get_many_by_name(names)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Skin',
                identifier='names',
                item_identifier=','.join(skin.name for skin in existence_skin_db_models))
            )
    return skin_db_models

@SKIN_ROUTER.get('/', response_model=None)
async def get_all(service_factory: DbServiceFactory) -> MsgResponseDTO | List[SkinModel]:
    skin_service = service_factory.get_skin_service()
    return list(await skin_service.get_all())


@SKIN_ROUTER.delete('/id')
async def delete_many_by_id(
        service_factory: DbServiceFactory, ids: List[int] = fastapi.Query(None)
):
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
                item_identifier=", ".join(str(id) for id in difference_ids))
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item='Skin',
                identifier='ids',
                item_identifier=', '.join(str(id) for id in ids)
            ))


@SKIN_ROUTER.delete('/name')
async def delete_many_by_name(
        service_factory: DbServiceFactory, names: List[str] = fastapi.Query(None)
):
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
                item_identifier=", ".join(name for name in difference_names))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item='Skin',
            identifier='names',
            item_identifier=', '.join(names))
        )

