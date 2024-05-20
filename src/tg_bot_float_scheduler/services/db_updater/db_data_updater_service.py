import asyncio


from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_scheduler.services.db_updater.db_data_sender_service import DbDataSenderService
from tg_bot_float_scheduler.services.db_updater.data_tree_from_source import DataTreeFromSource
from tg_bot_float_scheduler.services.db_updater.db_source_data_getter_service import DbSourceDataGetterService

class DbDataUpdaterService:
    def __init__(self, source_data_getter: DbSourceDataGetterService, db_data_sender: DbDataSenderService) -> None:
        self._source_data_getter = source_data_getter
        self._db_data_sender = db_data_sender

    async def update(self):
        datatree = DataTreeFromSource()
        async with self._source_data_getter:
            await self._process_datatree(datatree)
        await self._db_data_sender.send(datatree.to_dto())


    async def _process_datatree(self, datatree: DataTreeFromSource):
        tasks = []
        weapons = datatree.add_weapons(await self._source_data_getter.get_weapon_names())
        for weapon in weapons:
            task = asyncio.create_task(self._process_weapon_in_datatree(datatree, weapon))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_weapon_in_datatree(self, datatree: DataTreeFromSource, weapon: WeaponDTO):
        tasks = []
        skins = datatree.add_skins(
            await self._source_data_getter.get_skin_names(weapon.name)
        )
        for skin in skins:
            task = asyncio.create_task(self._process_weapon_skin_in_datatree(
                datatree, weapon, skin))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_weapon_skin_in_datatree(
            self, datatree: DataTreeFromSource, weapon: WeaponDTO, skin: SkinDTO,
    ):
        csm_wiki_skin_data = await self._source_data_getter.get_csm_wiki_skin_data(
            weapon.name, skin.name,
        )
        print(csm_wiki_skin_data)
        qualities = datatree.add_qualities(csm_wiki_skin_data["qualities"])
        skin.stattrak_existence = csm_wiki_skin_data["stattrak_existence"]
        for quality in qualities:
            datatree.add_relation(weapon, skin, quality)
