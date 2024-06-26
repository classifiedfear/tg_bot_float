import pickle
from typing import Dict, List, Tuple

import brotli


from tg_bot_float_db_app.database.services.quality_service import QualityService
from tg_bot_float_db_app.database.services.relation_service import RelationService
from tg_bot_float_db_app.database.services.skin_service import SkinService
from tg_bot_float_db_app.database.services.weapon_service import WeaponService

from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO
from tg_bot_float_common_dtos.schema_dtos.relation_id_dto import RelationIdDTO


class BotDBRefresherService:
    def __init__(
        self,
        weapon_service: WeaponService,
        skin_service: SkinService,
        quality_service: QualityService,
        relation_service: RelationService,
    ):
        self._weapon_service = weapon_service
        self._skin_service = skin_service
        self._quality_service = quality_service
        self._relation_service = relation_service

    async def update(self, request: bytes) -> None:
        """Update Weapon, Skin, Quality, Relations tables in database.

        Args:
            request (bytes): an object of SourceDataTreeDTO, pickled and compressed with brotli
        """
        db_dto = self._deserialize_request(request)
        await self._update_tables(db_dto)

    @staticmethod
    def _deserialize_request(request: bytes) -> SourceDataTreeDTO:
        to_unpickle = brotli.decompress(request)
        return pickle.loads(to_unpickle)

    async def _update_tables(self, db_dto: SourceDataTreeDTO) -> None:
        await self._update_weapons(db_dto.weapons)
        await self._update_skins(db_dto.skins)
        await self._update_qualities(db_dto.qualities)
        await self._update_relations(db_dto.relations)

    async def _update_weapons(self, weapons: List[WeaponDTO]) -> None:
        weapons_dtos_to_create, weapons_names_to_delete = (
            await self._get_weapon_dtos_to_create_and_names_to_delete(weapons)
        )
        if weapons_names_to_delete:
            await self._weapon_service.delete_many_by_name(weapons_names_to_delete)

        if weapons_dtos_to_create:
            weapon_db_models = await self._weapon_service.create_many(
                list(weapons_dtos_to_create.values())
            )

            for weapon_db_model in weapon_db_models:
                weapons_dtos_to_create[weapon_db_model.name].id = weapon_db_model.id

    async def _get_weapon_dtos_to_create_and_names_to_delete(
        self, weapons: List[WeaponDTO]
    ) -> Tuple[Dict[str, WeaponDTO], List[str]]:
        weapon_dtos_to_create = {weapon.name: weapon for weapon in weapons if weapon.name}
        weapon_names_to_delete: List[str] = []
        for weapon_db_model in await self._weapon_service.get_all():
            if weapon_dto := weapon_dtos_to_create.pop(weapon_db_model.name, None):
                weapon_dto.id = weapon_db_model.id
            else:
                weapon_names_to_delete.append(weapon_db_model.name)
        return weapon_dtos_to_create, weapon_names_to_delete

    async def _update_skins(self, skins: List[SkinDTO]) -> None:
        skin_dtos_to_create, skin_names_to_delete = (
            await self._get_skin_dtos_to_create_and_names_to_delete(skins)
        )
        if skin_names_to_delete:
            await self._skin_service.delete_many_by_name(skin_names_to_delete)

        if skin_dtos_to_create:
            skin_db_models = await self._skin_service.create_many(
                list(skin_dtos_to_create.values())
            )

            for skin_db_model in skin_db_models:
                skin_dtos_to_create[skin_db_model.name].id = skin_db_model.id

    async def _get_skin_dtos_to_create_and_names_to_delete(
        self, skins: List[SkinDTO]
    ) -> Tuple[Dict[str, SkinDTO], List[str]]:
        skin_dtos_to_create = {skin.name: skin for skin in skins if skin.name}
        skin_names_to_delete: List[str] = []
        for skin_db_model in await self._skin_service.get_all():
            if skin_dto := skin_dtos_to_create.pop(skin_db_model.name, None):
                skin_dto.id = skin_db_model.id
            else:
                skin_names_to_delete.append(skin_db_model.name)
        return skin_dtos_to_create, skin_names_to_delete

    async def _update_qualities(self, qualities: List[QualityDTO]) -> None:
        quality_dtos_to_create, quality_names_to_delete = (
            await self._get_quality_dtos_to_create_and_names_to_delete(qualities)
        )
        if quality_names_to_delete:
            await self._quality_service.delete_many_by_name(quality_names_to_delete)

        if quality_dtos_to_create:
            quality_db_models = await self._quality_service.create_many(
                list(quality_dtos_to_create.values())
            )

            for quality_db_model in quality_db_models:
                quality_dtos_to_create[quality_db_model.name].id = quality_db_model.id

    async def _get_quality_dtos_to_create_and_names_to_delete(
        self, qualities: List[QualityDTO]
    ) -> Tuple[Dict[str, QualityDTO], List[str]]:
        quality_dtos_to_create = {quality.name: quality for quality in qualities if quality.name}
        quality_names_to_delete: List[str] = []
        for quality_db_model in await self._quality_service.get_all():
            if quality_dto := quality_dtos_to_create.pop(quality_db_model.name, None):
                quality_dto.id = quality_db_model.id
            else:
                quality_names_to_delete.append(quality_db_model.name)
        return quality_dtos_to_create, quality_names_to_delete

    async def _update_relations(self, relations: List[RelationDTO]) -> None:
        ids_relations_to_create, ids_relations_to_delete = (
            await self._get_ids_relations_to_create_and_delete(relations)
        )
        if ids_relations_to_delete:
            await self._relation_service.delete_many_by_id(ids_relations_to_delete)

        if ids_relations_to_create:
            await self._relation_service.create_many(ids_relations_to_create)

    async def _get_ids_relations_to_create_and_delete(
        self, relations: List[RelationDTO]
    ) -> Tuple[List[RelationIdDTO], List[RelationIdDTO]]:
        ids_relations_to_create = [
            RelationIdDTO(
                weapon_id=relation.weapon.id,
                skin_id=relation.skin.id,
                quality_id=relation.quality.id,
            )
            for relation in relations
        ]
        ids_relations_to_delete: List[RelationIdDTO] = []
        for relation_db_model in await self._relation_service.get_all():
            if (
                relation_id_dto := RelationIdDTO(
                    weapon_id=relation_db_model.weapon_id,
                    skin_id=relation_db_model.skin_id,
                    quality_id=relation_db_model.quality_id,
                )
            ) in ids_relations_to_create:
                ids_relations_to_create.remove(relation_id_dto)
            else:
                ids_relations_to_delete.append(relation_id_dto)
        return ids_relations_to_create, ids_relations_to_delete
