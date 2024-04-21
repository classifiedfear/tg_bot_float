import pickle
from collections import namedtuple
import typing
import brotli

from tg_bot_float_db_app.database.bot_database_context import BotDatabaseContext
from tg_bot_float_db_app.database.tables import WeaponTable, SkinTable, QualityTable
from tg_bot_float_db_app.database.models import WeaponModel, SkinModel, QualityModel, RelationModel
from tg_bot_float_common_dtos import \
    ReceivedDataFromTreeDTO, WeaponDTO, SkinDTO, QualityDTO, RelationDTO


class BotDatabaseRefresher:
    def __init__(self, context: BotDatabaseContext):
        self._weapon_table = context.get_weapon_table()
        self._skin_table = context.get_skin_table()
        self._quality_table = context.get_quality_table()
        self._relations_table = context.get_weapon_skin_quality_table()

    async def refresh(self, request: bytes):
        db_dto = self._deserialize_request(request)
        await self._refresh_db(db_dto)

    @staticmethod
    def _deserialize_request(request: bytes):
        to_unpickle = brotli.decompress(request)
        return pickle.loads(to_unpickle)

    async def _refresh_db(self, db_dto: ReceivedDataFromTreeDTO):
        await self._update_weapons(db_dto.weapons)
        await self._update_skins(db_dto.skins)
        await self._update_qualities(db_dto.qualities)
        await self._update_relations(db_dto.relations)

    async def _update_weapons(self, weapons: typing.List[WeaponDTO]):
        weapons_dto_to_create, weapons_names_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            weapons, self._weapon_table
        )
        if weapons_names_to_delete or weapons_dto_to_create:
            if weapons_names_to_delete:
                await self._weapon_table.delete_many_by_name(weapons_names_to_delete)

            weapon_data_to_create = [
                WeaponModel(name=item.name) for item in weapons_dto_to_create.values()
               ]

            if weapon_data_to_create:
                await self._weapon_table.create_many(weapon_data_to_create)

            await self._weapon_table.save_changes()

            self._correct_ids_for_items_dto_by_models(weapons_dto_to_create, weapon_data_to_create)

    async def _update_skins(self, skins: typing.List[SkinDTO]):
        skins_dto_to_create, skin_names_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            skins, self._skin_table
        )
        if skin_names_to_delete or skins_dto_to_create:
            if skin_names_to_delete:
                await self._skin_table.delete_many_by_name(skin_names_to_delete)

            skin_models_to_create = [
                SkinModel(name=item.name, stattrak_existence=item.stattrak_existence)
                for item in skins_dto_to_create.values()
            ]

            if skin_models_to_create:
                await self._skin_table.create_many(skin_models_to_create)

            await self._skin_table.save_changes()

            self._correct_ids_for_items_dto_by_models(skins_dto_to_create, skin_models_to_create)

    async def _update_qualities(self, qualities: typing.List[QualityDTO]):
        qualities_dto_to_create, quality_names_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            qualities, self._quality_table
        )
        if quality_names_to_delete or qualities_dto_to_create:
            if quality_names_to_delete:
                await self._quality_table.delete_many_by_name(quality_names_to_delete)

            quality_model_to_create = [QualityModel(name=item.name) for item in qualities_dto_to_create.values()]

            if qualities_dto_to_create:
                await self._quality_table.create_many(quality_model_to_create)

            await self._quality_table.save_changes()

            self._correct_ids_for_items_dto_by_models(qualities_dto_to_create, quality_model_to_create)

    @staticmethod
    async def _get_items_dto_to_create_and_names_to_delete(
            items: typing.List[WeaponDTO] | typing.List[SkinDTO] | typing.List[QualityDTO],
            table: WeaponTable | SkinTable | QualityTable
    ):
        item_dto_to_create = {item.name: item for item in items}
        item_names_to_delete = []
        for item_db_model in await table.get_all():
            if item_dto := item_dto_to_create.pop(item_db_model.name, None):
                item_dto.id = item_db_model.id
            else:
                item_names_to_delete.append(item_db_model.name)
        return item_dto_to_create, item_names_to_delete

    @staticmethod
    def _correct_ids_for_items_dto_by_models(
        items_dto: typing.List[WeaponDTO] | typing.List[SkinDTO] | typing.List[QualityDTO], 
        items_models: typing.List[WeaponModel] | typing.List[SkinModel] |typing.List[QualityModel],
        ):
        for item_model in items_models:
            items_dto[item_model.name].id = item_model.id

    async def _update_relations(self, relations):
        ids_relations_to_create, ids_relations_to_delete = await self._get_ids_relations_to_create_and_delete(relations)
        if ids_relations_to_delete or ids_relations_to_create:
            if ids_relations_to_delete:
                await self._relations_table.delete_many_by_id(ids_relations_to_delete)

            wsq_model_relations_to_create = [
                RelationModel(weapon_id=relation.weapon_id, skin_id=relation.skin_id, quality_id=relation.quality_id)
                for relation in ids_relations_to_create
            ]

            if wsq_model_relations_to_create:
                await self._relations_table.create_many(wsq_model_relations_to_create)

            await self._relations_table.save_changes()

    async def _get_ids_relations_to_create_and_delete(self, relations: typing.List[RelationDTO]):
        relation_tuple = namedtuple('Relation', ['weapon_id', 'skin_id', 'quality_id'])
        ids_relations_to_create = {
            relation_tuple(relation.weapon.id, relation.skin.id, relation.quality.id) for relation in relations
        }
        ids_relations_to_delete = []
        for relation_db_model in await self._relations_table.get_all():
            if (relation_id_tuple := (
                    relation_db_model.weapon_id,
                    relation_db_model.skin_id,
                    relation_db_model.quality_id
            )) in ids_relations_to_create:
                ids_relations_to_create.remove(relation_id_tuple)
            else:
                ids_relations_to_delete.append(relation_id_tuple)
        return ids_relations_to_create, ids_relations_to_delete
