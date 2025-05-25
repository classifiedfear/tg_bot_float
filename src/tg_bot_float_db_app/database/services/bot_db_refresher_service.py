import pickle
from typing import List

import brotli


from tg_bot_float_common_dtos.update_db_scheduler_dtos.agent_relation_dto import AgentRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.glove_relation_dto import GloveRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO
from tg_bot_float_db_app.database.services.agent_service import AgentService
from tg_bot_float_db_app.database.services.dtos.db_refresher_dtos import (
    CreateDeleteDTO,
    IdRelationsCreateDeleteDTO,
)
from tg_bot_float_db_app.database.services.glove_service import GloveService
from tg_bot_float_db_app.database.services.quality_service import QualityService
from tg_bot_float_db_app.database.services.relation_service import RelationService
from tg_bot_float_db_app.database.services.skin_service import SkinService
from tg_bot_float_db_app.database.services.weapon_service import WeaponService

from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.relation_dto import RelationDTO


class BotDBRefresherService:
    def __init__(
        self,
        weapon_service: WeaponService,
        skin_service: SkinService,
        quality_service: QualityService,
        relation_service: RelationService,
        glove_service: GloveService,
        agent_service: AgentService,
    ):
        self._weapon_service = weapon_service
        self._skin_service = skin_service
        self._quality_service = quality_service
        self._relation_service = relation_service
        self._glove_service = glove_service
        self._agent_service = agent_service

    async def update(self, request: bytes) -> None:
        """Update Weapon, Skin, Quality, Relations tables in database.

        Args:
            request (bytes): an object of SourceDataTreeDTO, pickled and compressed with brotli
        """
        db_dto = self._deserialize_request(request)
        await self._update_tables(db_dto)

    @staticmethod
    def _deserialize_request(request: bytes) -> SourceDataTreeDTO:
        to_unpickle = brotli.decompress(request)  # type: ignore
        return pickle.loads(to_unpickle)  # type: ignore

    async def _update_tables(self, db_dto: SourceDataTreeDTO) -> None:
        await self._update_weapons(db_dto.weapons)
        await self._update_skins(db_dto.skins)
        await self._update_qualities(db_dto.qualities)
        await self._update_relations(db_dto.relations)
        await self._update_gloves(db_dto.gloves)
        await self._update_agents(db_dto.agents)
        await self._update_glove_relations(db_dto.glove_relations)
        await self._update_agent_relations(db_dto.agent_relations)

    async def _update_weapons(self, weapons: List[WeaponDTO]) -> None:
        create_delete_dto = await self._get_weapon_create_delete_dto(weapons)

        if to_delete := create_delete_dto.names_to_delete:
            await self._weapon_service.delete_many_by_name(to_delete)

        if to_create := create_delete_dto.dtos_to_create:
            weapon_db_models = await self._weapon_service.create_many(
                list(create_delete_dto.dtos_to_create.values())
            )

            for weapon_db_model in weapon_db_models:
                to_create[weapon_db_model.name].id = weapon_db_model.id

    async def _get_weapon_create_delete_dto(
        self, weapons: List[WeaponDTO]
    ) -> CreateDeleteDTO[WeaponDTO]:
        weapon_dtos_to_create = {weapon.name: weapon for weapon in weapons if weapon.name}
        weapon_names_to_delete: List[str] = []
        for weapon_db_model in await self._weapon_service.get_all():
            if weapon_dto := weapon_dtos_to_create.pop(weapon_db_model.name, None):
                weapon_dto.id = weapon_db_model.id
            else:
                weapon_names_to_delete.append(weapon_db_model.name)
        return CreateDeleteDTO(
            dtos_to_create=weapon_dtos_to_create, names_to_delete=weapon_names_to_delete
        )

    async def _update_skins(self, skins: List[SkinDTO]) -> None:
        create_delete_dto = await self._get_skin_create_delete_dto(skins)

        if to_delete := create_delete_dto.names_to_delete:
            await self._skin_service.delete_many_by_name(to_delete)

        if to_create := create_delete_dto.dtos_to_create:
            skin_db_models = await self._skin_service.create_many(list(to_create.values()))

            for skin_db_model in skin_db_models:
                to_create[skin_db_model.name].id = skin_db_model.id

    async def _get_skin_create_delete_dto(self, skins: List[SkinDTO]) -> CreateDeleteDTO[SkinDTO]:
        skin_dtos_to_create = {skin.name: skin for skin in skins if skin.name}
        skin_names_to_delete: List[str] = []
        for skin_db_model in await self._skin_service.get_all():
            if skin_dto := skin_dtos_to_create.pop(skin_db_model.name, None):
                skin_dto.id = skin_db_model.id
            else:
                skin_names_to_delete.append(skin_db_model.name)
        return CreateDeleteDTO(
            dtos_to_create=skin_dtos_to_create, names_to_delete=skin_names_to_delete
        )

    async def _update_qualities(self, qualities: List[QualityDTO]) -> None:
        create_delete_dto = await self._get_quality_create_delete_dto(qualities)

        if to_delete := create_delete_dto.names_to_delete:
            await self._quality_service.delete_many_by_name(to_delete)

        if to_create := create_delete_dto.dtos_to_create:
            quality_db_models = await self._quality_service.create_many(list(to_create.values()))

            for quality_db_model in quality_db_models:
                to_create[quality_db_model.name].id = quality_db_model.id

    async def _get_quality_create_delete_dto(
        self, qualities: List[QualityDTO]
    ) -> CreateDeleteDTO[QualityDTO]:
        quality_dtos_to_create = {quality.name: quality for quality in qualities if quality.name}
        quality_names_to_delete: List[str] = []
        for quality_db_model in await self._quality_service.get_all():
            if quality_dto := quality_dtos_to_create.pop(quality_db_model.name, None):
                quality_dto.id = quality_db_model.id
            else:
                quality_names_to_delete.append(quality_db_model.name)
        return CreateDeleteDTO(
            dtos_to_create=quality_dtos_to_create, names_to_delete=quality_names_to_delete
        )

    async def _update_relations(self, relations: List[RelationDTO]) -> None:
        id_relations_create_delete_dto = await self._get_ids_relations_create_delete_dto(relations)
        if to_delete := id_relations_create_delete_dto.ids_relations_to_delete:
            await self._relation_service.delete_many_by_id(to_delete)

        if to_create := id_relations_create_delete_dto.ids_relations_to_create:
            await self._relation_service.create_many(to_create)

    async def _get_ids_relations_create_delete_dto(
        self, relations: List[RelationDTO]
    ) -> IdRelationsCreateDeleteDTO:
        ids_relations_to_create = [
            RelationDTO(
                weapon_id=relation.weapon.id,
                skin_id=relation.skin.id,
                quality_id=relation.quality.id,
                stattrak_existence=relation.stattrak_existence,
            )
            for relation in relations
        ]
        ids_relations_to_delete: List[RelationDTO] = []
        for relation_db_model in await self._relation_service.get_all():
            if (
                relation_id_dto := RelationDTO(
                    weapon_id=relation_db_model.weapon_id,
                    skin_id=relation_db_model.skin_id,
                    quality_id=relation_db_model.quality_id,
                    stattrak_existence=relation_db_model.stattrak_existence,
                )
            ) in ids_relations_to_create:
                ids_relations_to_create.remove(relation_id_dto)
            else:
                ids_relations_to_delete.append(relation_id_dto)
        return IdRelationsCreateDeleteDTO(
            ids_relations_to_create=ids_relations_to_create,
            ids_relations_to_delete=ids_relations_to_delete,
        )

    async def _update_gloves(self, gloves: List[GloveDTO]) -> None:
        create_delete_dto = await self._get_glove_create_delete_dto(gloves)

        if to_delete := create_delete_dto.names_to_delete:
            await self._glove_service.delete_many_by_name(to_delete)

        if to_create := create_delete_dto.dtos_to_create:
            glove_db_models = await self._glove_service.create_many(list(to_create.values()))

            for glove_db_model in glove_db_models:
                to_create[glove_db_model.name].id = glove_db_model.id

    async def _get_glove_create_delete_dto(
        self, gloves: List[GloveDTO]
    ) -> CreateDeleteDTO[GloveDTO]:
        glove_dtos_to_create = {glove.name: glove for glove in gloves if glove.name}
        glove_names_to_delete: List[str] = []
        for glove_db_model in await self._glove_service.get_all():
            if glove_dto := glove_dtos_to_create.pop(glove_db_model.name, None):
                glove_dto.id = glove_db_model.id
            else:
                glove_names_to_delete.append(glove_db_model.name)
        return CreateDeleteDTO(
            dtos_to_create=glove_dtos_to_create, names_to_delete=glove_names_to_delete
        )

    async def _update_agents(self, agents: List[AgentDTO]) -> None:
        create_delete_dto = await self._get_agent_create_delete_dto(agents)

        if to_delete := create_delete_dto.names_to_delete:
            await self._agent_service.delete_many_by_name(to_delete)

        if to_create := create_delete_dto.dtos_to_create:
            agent_db_models = await self._agent_service.create_many(list(to_create.values()))

            for agent_db_model in agent_db_models:
                to_create[agent_db_model.name].id = agent_db_model.id

    async def _get_agent_create_delete_dto(
        self, agents: List[AgentDTO]
    ) -> CreateDeleteDTO[AgentDTO]:
        agent_dtos_to_create = {agent.name: agent for agent in agents if agent.name}
        agent_names_to_delete: List[str] = []
        for agent_db_model in await self._agent_service.get_all():
            if agent_dto := agent_dtos_to_create.pop(agent_db_model.name, None):
                agent_dto.id = agent_db_model.id
            else:
                agent_names_to_delete.append(agent_db_model.name)
        return CreateDeleteDTO(
            dtos_to_create=agent_dtos_to_create, names_to_delete=agent_names_to_delete
        )

    async def _update_glove_relations(self, glove_relations: List[GloveRelationDTO]) -> None:
        for glove_relation in glove_relations:
            glove_db_model = await self._glove_service.get_by_name(str(glove_relation.glove.name))
            skin_db_models = await self._skin_service.get_many_by_name(
                [str(skin.name) for skin in glove_relation.skins]
            )
            await self._glove_service.update_relations(glove_db_model, list(skin_db_models))

    async def _update_agent_relations(self, agent_relations: List[AgentRelationDTO]) -> None:
        for agent_relation in agent_relations:
            agent_db_model = await self._agent_service.get_by_name(str(agent_relation.agent.name))
            skin_db_models = await self._skin_service.get_many_by_name(
                [str(skin.name) for skin in agent_relation.skins]
            )
            await self._agent_service.update_relations(agent_db_model, list(skin_db_models))
