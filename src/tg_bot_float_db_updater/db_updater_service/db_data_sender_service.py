import pickle

from aiohttp import ClientSession
import brotli

from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO


class DbDataSenderService:
    def __init__(self, settings: DbUpdaterSettings) -> None:
        self._settings = settings

    async def send(self, db_dto: SourceDataTreeDTO) -> None:
        async with ClientSession() as session:
            bytes_db_dto = pickle.dumps(db_dto)
            compressed_db_dto = brotli.compress(bytes_db_dto)
            async with session.post(
                self._settings.db_update_url,
                data=compressed_db_dto,
            ) as response:
                assert response.status in list(range(200, 300))
