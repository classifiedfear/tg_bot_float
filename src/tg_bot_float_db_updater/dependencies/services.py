from functools import lru_cache
from typing import Annotated

from fastapi import Depends


from tg_bot_float_db_updater.db_updater_service.db_source_data_getter_service import (
    DbSourceDataGetterService,
)
from tg_bot_float_db_updater.db_updater_service.db_data_updater_service import DbDataUpdaterService
from tg_bot_float_db_updater.db_updater_service.db_data_sender_service import DbDataSenderService
from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings


@lru_cache
def get_db_updater_settings() -> DbUpdaterSettings:
    return DbUpdaterSettings()


DB_UPDATER_SETTINGS = Annotated[DbUpdaterSettings, Depends(get_db_updater_settings)]


async def get_updater_service(settings: DB_UPDATER_SETTINGS):
    db_data_getter_service = DbSourceDataGetterService(settings)
    db_data_sender_service = DbDataSenderService(settings)
    db_updater_service = DbDataUpdaterService(db_data_getter_service, db_data_sender_service)
    try:
        yield db_updater_service
    finally:
        await db_data_getter_service.close_session()


DB_UPDATER_SERVICE = Annotated[DbDataUpdaterService, Depends(get_updater_service)]
