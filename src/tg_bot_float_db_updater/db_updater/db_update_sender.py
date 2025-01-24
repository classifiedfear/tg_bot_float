import pickle
from typing import Self

from aiohttp import ClientSession
import brotli  # type: ignore

from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO


class DbUpdateSender:
    _success_statuses = list(range(200, 300))

    def __init__(self, settings: DbUpdaterSettings, session: ClientSession) -> None:
        self._settings = settings
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        await self._session.close()

    async def send(self, db_dto: SourceDataTreeDTO) -> None:
        bytes_db_dto = pickle.dumps(db_dto)
        compressed_db_dto = brotli.compress(bytes_db_dto)  # type: ignore
        async with self._session.post(
            self._settings.db_update_url,
            data=compressed_db_dto,
        ) as response:
            assert response.status in self._success_statuses
