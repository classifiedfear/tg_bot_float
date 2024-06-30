from functools import lru_cache
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends


from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.csm_wiki_source_getter_service import (
    CsmWikiSourceGetterService,
)
from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.db_source_data_getter_service import (
    CsgoDbSourceGetterService,
)
from tg_bot_float_db_updater.db_updater_service.db_data_updater_service import DbDataUpdaterService
from tg_bot_float_db_updater.db_updater_service.db_data_sender_service import DbDataSenderService
from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings


@lru_cache
def get_db_updater_settings() -> DbUpdaterSettings:
    return DbUpdaterSettings()


DB_UPDATER_SETTINGS = Annotated[DbUpdaterSettings, Depends(get_db_updater_settings)]


async def get_aiohttp_session():
    async with ClientSession() as session:
        yield session


async def get_updater_service(
    settings: DB_UPDATER_SETTINGS, aiohttp_session: ClientSession = Depends(get_aiohttp_session)
):
    async with CsgoDbSourceGetterService(
        settings, aiohttp_session
    ) as csgo_db, CsmWikiSourceGetterService(
        settings, aiohttp_session
    ) as csm_wiki, DbDataSenderService(
        settings, aiohttp_session
    ) as db_sender:
        db_updater_service = DbDataUpdaterService(
            csgo_db,
            csm_wiki,
            db_sender,
        )
        try:
            yield db_updater_service
        finally:
            await aiohttp_session.close()


DB_UPDATER_SERVICE = Annotated[DbDataUpdaterService, Depends(get_updater_service)]
