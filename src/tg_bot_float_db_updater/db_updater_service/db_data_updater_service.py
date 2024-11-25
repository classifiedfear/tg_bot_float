import asyncio
from typing import Awaitable, Dict, List

from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_db_updater.db_updater_service.db_data_sender_service import DbDataSenderService
from tg_bot_float_db_updater.db_updater_service.data_tree_from_source import DataTreeFromSource
from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.csm_wiki_source_getter_service import (
    CsmWikiSourceGetterService,
)
from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.csgo_db_source_getter_service import (
    CsgoDbSourceGetterService,
)


class DbDataUpdaterService:
    def __init__(
        self,
        csgo_db_source_getter_service: CsgoDbSourceGetterService,
        csm_wiki_source_getter_service: CsmWikiSourceGetterService,
        db_data_sender: DbDataSenderService,
    ) -> None:
        self._source_data_getter = csgo_db_source_getter_service
        self._csm_wiki_source_getter_service = csm_wiki_source_getter_service
        self._db_data_sender = db_data_sender

    async def update(self) -> None:
        datatree = DataTreeFromSource()
        await self._process_datatree(datatree)
        dto_to_send = datatree.to_dto()
        await self._db_data_sender.send(dto_to_send)

    async def _process_datatree(self, datatree: DataTreeFromSource) -> None:
        await asyncio.gather(
            self._process_agents_in_datatree(datatree),
            self._process_gloves_in_datatree(datatree),
            self._process_weapons_in_datatree(datatree),
        )

    async def _process_gloves_in_datatree(self, datatree: DataTreeFromSource) -> None:
        gloves_page_dtos = await self._source_data_getter.get_gloves_page()
        gloves_relations: Dict[str, List[SkinDTO]] = {}
        for glove_page in gloves_page_dtos:
            glove_skin_dtos: List[SkinDTO] = datatree.add_skins(glove_page.skins)
            gloves_relations[glove_page.glove_name] = glove_skin_dtos
        glove_dtos: List[GloveDTO] = datatree.add_gloves(list(gloves_relations.keys()))
        for glove_dto in glove_dtos:
            for glove_skin_dto in gloves_relations[str(glove_dto.name)]:
                datatree.add_glove_relations(glove_dto, glove_skin_dto)

    async def _process_agents_in_datatree(self, datatree: DataTreeFromSource) -> None:
        agents_page_dtos: List[AgentsPageDTO] = await self._source_data_getter.get_agents_page()
        agent_relations: Dict[str, List[SkinDTO]] = {}
        for agent_page in agents_page_dtos:
            agent_skin_dtos: List[SkinDTO] = datatree.add_skins(agent_page.skins)
            agent_relations[agent_page.fraction_name] = agent_skin_dtos
        agent_dtos: List[AgentDTO] = datatree.add_agents(list(agent_relations.keys()))
        for agent_dto in agent_dtos:
            for agent_skin_dto in agent_relations[str(agent_dto.name)]:
                datatree.add_agent_relations(agent_dto, agent_skin_dto)

    async def _process_weapons_in_datatree(self, datatree: DataTreeFromSource) -> None:
        tasks: List[Awaitable[None]] = []
        weapons_page = await self._source_data_getter.get_weapons_page()
        weapon_dtos: List[WeaponDTO] = datatree.add_weapons(
            weapons_page.weapons + weapons_page.knives + weapons_page.other
        )
        for weapon_dto in weapon_dtos:
            task = asyncio.create_task(
                self._process_skins_for_weapon_in_datatree(datatree, weapon_dto)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_skins_for_weapon_in_datatree(
        self, datatree: DataTreeFromSource, weapon_dto: WeaponDTO
    ) -> None:
        tasks: List[Awaitable[None]] = []
        skins_page = await self._source_data_getter.get_skins_page(str(weapon_dto.name))
        skin_dtos = datatree.add_skins(skins_page.skins)
        for skin_dto in skin_dtos:
            task = asyncio.create_task(
                self._process_qualities_stattrak_for_weapon_skin_in_datattree(
                    datatree, weapon_dto, skin_dto
                )
            )
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_qualities_stattrak_for_weapon_skin_in_datattree(
        self,
        datatree: DataTreeFromSource,
        weapon_dto: WeaponDTO,
        skin_dto: SkinDTO,
    ) -> None:
        csm_wiki_dto = await self._csm_wiki_source_getter_service.get_csm_wiki_skin_data(
            str(weapon_dto.name),
            str(skin_dto.name),
        )
        quality_dtos: List[QualityDTO] = datatree.add_qualities(csm_wiki_dto.qualities)
        skin_dto.stattrak_existence = csm_wiki_dto.stattrak_existence
        for quality_dto in quality_dtos:
            datatree.add_relation(weapon_dto, skin_dto, quality_dto)
