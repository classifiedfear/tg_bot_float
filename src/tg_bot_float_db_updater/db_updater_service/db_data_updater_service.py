import asyncio
from typing import Awaitable, List

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
        await self._db_data_sender.send(datatree.to_dto())

    async def _process_datatree(self, datatree: DataTreeFromSource) -> None:
        await self._process_gloves_agents_in_datatree(datatree)
        await self._process_weapons_in_datatree(datatree)

    async def _process_gloves_agents_in_datatree(self, datatree: DataTreeFromSource) -> None:
        gloves_page_dtos, agents_page_dtos = await asyncio.gather(
            self._source_data_getter.get_gloves_page(), self._source_data_getter.get_agents_page()
        )
        datatree.add_gloves(gloves_page_dtos)
        datatree.add_agents(agents_page_dtos)

    async def _process_weapons_in_datatree(self, datatree: DataTreeFromSource) -> None:
        tasks: List[Awaitable[None]] = []
        weapons_page = await self._source_data_getter.get_weapons_page()
        weapons = datatree.add_weapons(
            weapons_page.weapons + weapons_page.knives + weapons_page.other
        )
        for weapon in weapons:
            task = asyncio.create_task(self._process_skins_for_weapon_in_datatree(datatree, weapon))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_skins_for_weapon_in_datatree(
        self, datatree: DataTreeFromSource, weapon: WeaponDTO
    ) -> None:
        tasks: List[Awaitable[None]] = []
        skins_page = await self._source_data_getter.get_skins_page(str(weapon.name))
        skins = datatree.add_skins(skins_page.skins)
        for skin in skins:
            task = asyncio.create_task(
                self._process_qualities_stattrak_for_weapon_skin_in_datattree(
                    datatree, weapon, skin
                )
            )
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_qualities_stattrak_for_weapon_skin_in_datattree(
        self,
        datatree: DataTreeFromSource,
        weapon: WeaponDTO,
        skin: SkinDTO,
    ) -> None:
        csm_wiki_dto = await self._csm_wiki_source_getter_service.get_csm_wiki_skin_data(
            str(weapon.name),
            str(skin.name),
        )
        qualities = datatree.add_qualities(csm_wiki_dto.qualities)
        skin.stattrak_existence = csm_wiki_dto.stattrak_existence
        for quality in qualities:
            datatree.add_relation(weapon, skin, quality)
