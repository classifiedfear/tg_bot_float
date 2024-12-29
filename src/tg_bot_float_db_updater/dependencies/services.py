from functools import lru_cache
from typing import Annotated, AsyncGenerator, Any

from aiohttp import ClientSession
from fastapi import Depends


from tg_bot_float_db_updater.db_updater.source_data_getter.csm_wiki_source_getter_service import (
    CsmWikiSourceGetter,
)
from tg_bot_float_db_updater.db_updater.source_data_getter.csgo_db_source_getter import (
    CsgoDbSourceDataGetter,
)
from tg_bot_float_db_updater.db_updater.db_updater_service import DbUpdaterService
from tg_bot_float_db_updater.db_updater.db_update_sender import DbUpdateSender
from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings


@lru_cache
def get_db_updater_settings() -> DbUpdaterSettings:
    return DbUpdaterSettings()  # type: ignore "Load variables from db_updater_variables.env file"


DB_UPDATER_SETTINGS = Annotated[DbUpdaterSettings, Depends(get_db_updater_settings)]


async def get_aiohttp_session() -> AsyncGenerator[ClientSession, Any]:
    async with ClientSession() as session:
        yield session


async def get_updater_service(
    settings: DB_UPDATER_SETTINGS, aiohttp_session: ClientSession = Depends(get_aiohttp_session)
) -> AsyncGenerator[DbUpdaterService, Any]:
    async with CsgoDbSourceDataGetter(
        settings, aiohttp_session
    ) as csgo_db, CsmWikiSourceGetter(settings, aiohttp_session) as csm_wiki, DbUpdateSender(
        settings, aiohttp_session
    ) as db_sender:
        db_updater_service = DbUpdaterService(
            csgo_db,
            csm_wiki,
            db_sender,
        )
        try:
            yield db_updater_service
        finally:
            await aiohttp_session.close()


DB_UPDATER_SERVICE = Annotated[DbUpdaterService, Depends(get_updater_service)]
