from typing import List

import fastapi
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import ITEM_EXIST_MSG, ITEM_NOT_EXIST_MSG, \
    ITEM_DELETED_MSG
from tg_bot_float_common_dtos.quality_dto import QualityDTO
from tg_bot_float_db_app.api.dependencies.service_factory import DbServiceFactory

QUALITY_ROUTER = fastapi.APIRouter(prefix="/qualities", tags=["qualities"])


@QUALITY_ROUTER.post('/create', response_model=None)
async def create(
        service_factory: DbServiceFactory, quality_dto: QualityDTO) -> MsgResponseDTO | QualityModel:
    quality_service = service_factory.get_quality_service()
    try:
        quality_db_model = await quality_service.create(quality_dto)
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Quality', identifier='name', item_identifier=quality_dto.name)
            )
    return quality_db_model


@QUALITY_ROUTER.get('/id/{quality_id}', response_model=None)
async def get_quality_by_id(
        service_factory: DbServiceFactory, quality_id: int) -> MsgResponseDTO | QualityModel:
    quality_service = service_factory.get_quality_service()
    if quality_db_model := await quality_service.get_by_id(quality_id):
        return quality_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(
            item='Quality', identifier='id', item_identifier=str(quality_id)
            ))

@QUALITY_ROUTER.put('/id/{quality_id}', response_model=None)
async def update_quality_by_id(
        service_factory: DbServiceFactory, quality_id: int, quality_dto: QualityDTO) -> MsgResponseDTO | QualityModel:
    quality_service = service_factory.get_quality_service()
    try:
        if (quality_db_model := await quality_service.update_by_id(quality_id, quality_dto)) is None:
            return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Quality', identifier='id', item_identifier=str(quality_id)
                )
            )
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Quality', identifier='name', item_name=quality_dto.name
                )
            )
    return quality_db_model

@QUALITY_ROUTER.delete('/id/{quality_id}')
async def delete_quality_by_id(
        service_factory: DbServiceFactory, quality_id: int) -> MsgResponseDTO:
    quality_service = service_factory.get_quality_service()
    try:
        await quality_service.delete_by_id(quality_id)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Quality',
                identifier='id',
                item_identifier=str(quality_id))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item="Quality",
            identifier='id',
            item_identifier=str(quality_id))
        )


@QUALITY_ROUTER.get('/name/{quality_name}', response_model=None)
async def get_quality_by_name(service_factory: DbServiceFactory, quality_name: str) -> MsgResponseDTO | QualityModel:
    quality_service = service_factory.get_quality_service()
    if quality_db_model := await quality_service.get_by_name(quality_name):
        return quality_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(item='Quality', identifier='name', item_identifier=quality_name)
        )


@QUALITY_ROUTER.put('/name/{quality_name}', response_model=None)
async def update_quality_by_name(
        service_factory: DbServiceFactory, quality_name: str, quality_dto: QualityDTO,
) -> MsgResponseDTO | QualityModel:
    quality_service = service_factory.get_quality_service()
    try:
        if (quality_db_model := await quality_service.update_by_name(quality_name, quality_dto)) is None:
            return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Quality', identifier='name', item_identifier=quality_name)
            )
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Quality', identifier='name', itet_identifier=quality_dto.name
                )
            )
    return quality_db_model


@QUALITY_ROUTER.delete('/name/{quality_name}')
async def delete_quality_by_name(service_factory: DbServiceFactory, quality_name: str) -> MsgResponseDTO:
    quality_service = service_factory.get_quality_service()
    try:
        await quality_service.delete_by_name(quality_name)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Quality', identifier='name', item_identifier=quality_name)
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item="Quality", identifier='name', item_identifier=quality_name)
            )


@QUALITY_ROUTER.post('/create_many', response_model=None)
async def create_many(
        service_factory: DbServiceFactory, quality_dtos: List[QualityDTO]) -> MsgResponseDTO | List[QualityModel]:
    quality_service = service_factory.get_quality_service()
    try:
        quality_db_models = await quality_service.create_many(quality_dtos)
    except IntegrityError:
        names = [quality_dto.name for quality_dto in quality_dtos]
        existence_quality_db_models = await quality_service.get_many_by_name(names)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Quality',
                identifier='names',
                item_identifier=','.join(quality.name for quality in existence_quality_db_models))
            )
    return quality_db_models


@QUALITY_ROUTER.get('/', response_model=None)
async def get_all(service_factory: DbServiceFactory) -> List[QualityModel]:
    quality_service = service_factory.get_quality_service()
    return list(await quality_service.get_all())


@QUALITY_ROUTER.delete('/id')
async def delete_many_by_id(
        service_factory: DbServiceFactory, ids: List[int] = fastapi.Query(None)) -> MsgResponseDTO:
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
                item_identifier=", ".join(str(id) for id in difference_ids))
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item='Quality',
                identifier='ids',
                item_identifier=', '.join(str(id) for id in ids)
            ))


@QUALITY_ROUTER.delete('/name')
async def delete_many_by_name(
        service_factory: DbServiceFactory, names: List[str] = fastapi.Query(None)) -> MsgResponseDTO:
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
                item_identifier=", ".join(name for name in difference_names))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item='Quality',
            identifier='names',
            item_identifier=', '.join(names))
        )

