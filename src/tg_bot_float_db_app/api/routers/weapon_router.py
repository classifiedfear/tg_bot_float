from typing import List

import fastapi
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.misc.router_constants import ITEM_EXIST_MSG, ITEM_NOT_EXIST_MSG, \
    ITEM_DELETED_MSG
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO
from tg_bot_float_db_app.api.dependencies.service_factory import DbServiceFactory


WEAPON_ROUTER = fastapi.APIRouter(prefix="/weapons", tags=["weapons"])


@WEAPON_ROUTER.post('/create', response_model=None)
async def create(
        service_factory: DbServiceFactory, weapon_dto: WeaponDTO
) -> MsgResponseDTO | WeaponModel:
    weapon_service = service_factory.get_weapon_service()
    try:
        weapon_db_model = await weapon_service.create(weapon_dto)
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Weapon', identifier='name', item_identifier=weapon_dto.name)
            )
    return weapon_db_model


@WEAPON_ROUTER.get('/id/{weapon_id}', response_model=None)
async def get_weapon_by_id(
        service_factory: DbServiceFactory, weapon_id: int
) -> MsgResponseDTO | WeaponModel:
    weapon_service = service_factory.get_weapon_service()
    if weapon_db_model := await weapon_service.get_by_id(weapon_id):
        return weapon_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(item='Weapon', identifier='id', item_identifier=str(weapon_id)))

@WEAPON_ROUTER.put('/id/{weapon_id}', response_model=None)
async def update_weapon_by_id(
        service_factory: DbServiceFactory, weapon_id: int, weapon_dto: WeaponDTO
) -> MsgResponseDTO | WeaponModel:
    weapon_service = service_factory.get_weapon_service()
    try:
        if (weapon_db_model := await weapon_service.update_by_id(weapon_id, weapon_dto)) is None:
            return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(item='Weapon', identifier='id', item_identifier=str(weapon_id)))
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Weapon', identifier='name', item_name=weapon_dto.name)
            )
    return weapon_db_model

@WEAPON_ROUTER.delete('/id/{weapon_id}')
async def delete_weapon_by_id(
        service_factory: DbServiceFactory, weapon_id: int
) -> MsgResponseDTO:
    weapon_service = service_factory.get_weapon_service()
    try:
        await weapon_service.delete_by_id(weapon_id)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Weapon',
                identifier='id',
                item_identifier=str(weapon_id))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item="Weapon",
            identifier='id',
            item_identifier=str(weapon_id))
        )

@WEAPON_ROUTER.get('/name/{weapon_name}', response_model=None)
async def get_weapon_by_name(
        service_factory: DbServiceFactory, weapon_name: str
) -> MsgResponseDTO | WeaponModel:
    weapon_service = service_factory.get_weapon_service()
    if weapon_db_model := await weapon_service.get_by_name(weapon_name):
        return weapon_db_model
    return MsgResponseDTO(
        status=False,
        msg=ITEM_NOT_EXIST_MSG.format(item='Weapon', identifier='name', item_identifier=weapon_name)
        )


@WEAPON_ROUTER.put('/name/{weapon_name}', response_model=None)
async def update_weapon_by_name(
        service_factory: DbServiceFactory, weapon_name: str, weapon_dto: WeaponDTO
) -> MsgResponseDTO | WeaponModel:
    weapon_service = service_factory.get_weapon_service()
    try:
        if (weapon_db_model := await weapon_service.update_by_name(weapon_name, weapon_dto)) is None:
            return MsgResponseDTO(
                    status=False,
                    msg=ITEM_NOT_EXIST_MSG.format(item='Weapon', identifier='name', item_identifier=weapon_name)
                )
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(item='Weapon', identifier='name', item_identifier=weapon_name)
            )
    return weapon_db_model


@WEAPON_ROUTER.delete('/name/{weapon_name}')
async def delete_weapon_by_name(
        service_factory: DbServiceFactory, weapon_name: str
):
    weapon_service = service_factory.get_weapon_service()
    try:
        await weapon_service.delete_by_name(weapon_name)
    except BotDbDeleteException:
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item='Weapon', identifier='name', item_identifier=weapon_name)
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item="Weapon", identifier='name', item_identifier=weapon_name)
            )


@WEAPON_ROUTER.post('/create_many', response_model=None)
async def create_many(
        service_factory: DbServiceFactory, weapon_dtos: List[WeaponDTO]
) -> MsgResponseDTO | List[WeaponModel]:
    weapon_service = service_factory.get_weapon_service()
    try:
        weapon_db_models = await weapon_service.create_many(weapon_dtos)
    except IntegrityError:
        names = [weapon.name for weapon in weapon_dtos]
        existence_weapon_db_models = await weapon_service.get_many_by_name(names)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_EXIST_MSG.format(
                item='Weapon',
                identifier='names',
                item_identifier=','.join(weapon.name for weapon in existence_weapon_db_models))
            )
    return weapon_db_models


@WEAPON_ROUTER.get('/', response_model=None)
async def get_all(service_factory: DbServiceFactory) -> MsgResponseDTO | List[WeaponModel]:
    weapon_service = service_factory.get_weapon_service()
    return list(await weapon_service.get_all())


@WEAPON_ROUTER.delete('/id')
async def delete_many_by_id(
        service_factory: DbServiceFactory, ids: List[int] = fastapi.Query(None)
) -> MsgResponseDTO:
    weapon_service = service_factory.get_weapon_service()
    try:
        await weapon_service.delete_many_by_id(ids)
    except BotDbDeleteException:
        existence_weapon_db_models = await weapon_service.get_many_by_id(ids)
        existence_ids = {weapon.id for weapon in existence_weapon_db_models}
        difference_ids = set(ids).symmetric_difference(existence_ids)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item="Weapon",
                identifier="ids",
                item_identifier=", ".join(str(id) for id in difference_ids))
            )
    return MsgResponseDTO(
            status=True,
            msg=ITEM_DELETED_MSG.format(
                item='Weapon',
                identifier='ids',
                item_identifier=', '.join(str(id) for id in ids)
            ))


@WEAPON_ROUTER.delete('/name')
async def delete_many_by_name(
        service_factory: DbServiceFactory, names: List[str] = fastapi.Query(None)
) -> MsgResponseDTO:
    weapon_service = service_factory.get_weapon_service()
    try:
        await weapon_service.delete_many_by_name(names)
    except BotDbDeleteException:
        existence_weapon_db_models = await weapon_service.get_many_by_name(names)
        existence_names = {weapon.name for weapon in existence_weapon_db_models}
        difference_names = set(names).symmetric_difference(existence_names)
        return MsgResponseDTO(
            status=False,
            msg=ITEM_NOT_EXIST_MSG.format(
                item="Weapon",
                identifier="names",
                item_identifier=", ".join(name for name in difference_names))
            )
    return MsgResponseDTO(
        status=True,
        msg=ITEM_DELETED_MSG.format(
            item='Weapon',
            identifier='names',
            item_identifier=', '.join(names))
        )
