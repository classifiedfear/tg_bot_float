from typing import List

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Query


from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.misc.exceptions import BotDbDeleteException
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY
from tg_bot_float_db_app.misc.router_constants import ITEM_EXIST_MSG, ITEM_NOT_EXIST_MSG, \
    ITEM_DELETED_MSG
from tg_bot_float_common_dtos.weapon_dto import WeaponDTO


class WeaponRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/weapons", tags=["weapons"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/create", self._create, response_model=None, methods=["POST"])
        self._router.add_api_route(
            "/id/{weapon_id}", self._get_weapon_by_id, response_model=None, methods=["GET"]
            )
        self._router.add_api_route(
            "/id/{weapon_id}", self._update_weapon_by_id, response_model=None, methods=["PUT"]
            )
        self._router.add_api_route(
            "/id/{weapon_id}", self._delete_weapon_by_id, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._get_weapon_by_name, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._update_weapon_by_name, response_model=None, methods=["PUT"]
        )
        self._router.add_api_route(
            "/name/{weapon_name}", self._delete_weapon_by_name, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/create_many", self._create_many, response_model=None, methods=["POST"]
        )
        self._router.add_api_route(
            "/", self._get_all, response_model=None, methods=["GET"]
        )
        self._router.add_api_route(
            "/id", self._delete_many_by_id, methods=["DELETE"]
        )
        self._router.add_api_route(
            "/name", self._delete_many_by_name, methods=["DELETE"]
        )


    async def _create(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_dto: WeaponDTO
        ) -> MsgResponseDTO | WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                weapon_db_model = await weapon_service.create(weapon_dto)
            except IntegrityError:
                return MsgResponseDTO(status=False, msg=ITEM_EXIST_MSG.format(
                    item='Weapon',
                    identifier='name',
                    item_identifier=weapon_dto.name))
            return weapon_db_model

    async def _get_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
        ) -> MsgResponseDTO | WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            if weapon_db_model := await weapon_service.get_by_id(weapon_id):
                return weapon_db_model
            return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                item='Weapon',
                identifier='id',
                item_identifier=str(weapon_id)))

    async def _update_weapon_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_id: int,
        weapon_dto: WeaponDTO
        ) -> MsgResponseDTO | WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                if (
                    weapon_db_model := await weapon_service.update_by_id(weapon_id, weapon_dto)
                    ) is None:
                    return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                        item='Weapon',
                        identifier='id',
                        item_identifier=str(weapon_id)))
            except IntegrityError:
                return MsgResponseDTO(status=False, msg=ITEM_EXIST_MSG.format(
                    item='Weapon',
                    identifier='name',
                    item_name=weapon_dto.name))
            return weapon_db_model

    async def _delete_weapon_by_id(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_id: int
        ) -> MsgResponseDTO:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                await weapon_service.delete_by_id(weapon_id)
            except BotDbDeleteException:
                return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                        item='Weapon',
                        identifier='id',
                        item_identifier=str(weapon_id)))
            return MsgResponseDTO(status=True, msg=ITEM_DELETED_MSG.format(
                    item="Weapon",
                    identifier='id',
                    item_identifier=str(weapon_id)))

    async def _get_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
        ) -> MsgResponseDTO | WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            if weapon_db_model := await weapon_service.get_by_name(weapon_name):
                return weapon_db_model
            return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                item='Weapon',
                identifier='name',
                item_identifier=weapon_name))


    async def _update_weapon_by_name(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        weapon_name: str,
        weapon_dto: WeaponDTO
        ) -> MsgResponseDTO | WeaponModel:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                if (
                    weapon_db_model := await weapon_service.update_by_name(weapon_name, weapon_dto)
                    ) is None:
                    return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                        item='Weapon',
                        identifier='name',
                        item_identifier=weapon_name))
            except IntegrityError:
                return MsgResponseDTO(status=False, msg=ITEM_EXIST_MSG.format(
                    item='Weapon', identifier='name', item_identifier=weapon_name))
            return weapon_db_model

    async def _delete_weapon_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_name: str
        ) -> MsgResponseDTO:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                await weapon_service.delete_by_name(weapon_name)
            except BotDbDeleteException:
                return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                    item='Weapon',
                    identifier='name',
                    item_identifier=weapon_name))
            return MsgResponseDTO(status=True, msg=ITEM_DELETED_MSG.format(
                    item="Weapon", identifier='name', item_identifier=weapon_name))

    async def _create_many(
        self, service_factory: BOT_DB_SERVICE_FACTORY, weapon_dtos: List[WeaponDTO]
        ) -> MsgResponseDTO | List[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                weapon_db_models = await weapon_service.create_many(weapon_dtos)
            except IntegrityError:
                names = [weapon.name for weapon in weapon_dtos]
                existence_weapon_db_models = await weapon_service.get_many_by_name(names)
                return MsgResponseDTO(status=False, msg=ITEM_EXIST_MSG.format(
                    item='Weapon',
                    identifier='names',
                    item_identifier=','.join(weapon.name for weapon in existence_weapon_db_models)))
            return weapon_db_models

    async def _get_all(
        self, service_factory: BOT_DB_SERVICE_FACTORY
        ) -> MsgResponseDTO | List[WeaponModel]:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            return list(await weapon_service.get_all())

    async def _delete_many_by_id(
        self,
        service_factory: BOT_DB_SERVICE_FACTORY,
        ids: List[int] = Query(None)
        ) -> MsgResponseDTO:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                await weapon_service.delete_many_by_id(ids)
            except BotDbDeleteException:
                existence_weapon_db_models = await weapon_service.get_many_by_id(ids)
                existence_ids = {weapon.id for weapon in existence_weapon_db_models}
                difference_ids = set(ids).symmetric_difference(existence_ids)
                return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                    item="Weapon",
                    identifier="ids",
                    item_identifier=", ".join(str(id) for id in difference_ids)))
            return MsgResponseDTO(status=True,msg=ITEM_DELETED_MSG.format(
                    item='Weapon',
                    identifier='ids',
                    item_identifier=', '.join(str(id) for id in ids)))

    async def _delete_many_by_name(
        self, service_factory: BOT_DB_SERVICE_FACTORY, names: List[str] = Query(None)
        ) -> MsgResponseDTO:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            try:
                await weapon_service.delete_many_by_name(names)
            except BotDbDeleteException:
                existence_weapon_db_models = await weapon_service.get_many_by_name(names)
                existence_names = {weapon.name for weapon in existence_weapon_db_models}
                difference_names = set(names).symmetric_difference(existence_names)
                return MsgResponseDTO(status=False, msg=ITEM_NOT_EXIST_MSG.format(
                        item="Weapon",
                        identifier="names",
                        item_identifier=", ".join(name for name in difference_names))
                    )
            return MsgResponseDTO(status=True, msg=ITEM_DELETED_MSG.format(
                    item='Weapon',
                    identifier='names',
                    item_identifier=', '.join(names)))
