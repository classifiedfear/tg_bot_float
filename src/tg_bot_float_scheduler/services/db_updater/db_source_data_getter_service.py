from typing import List

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from settings.update_db_scheduler_settings import SchedulerSettings


class DbSourceDataGetterService:
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(self, settings: SchedulerSettings) -> None:
        self._settings = settings

    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    async def get_weapon_names(self) -> List[str]:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            self._settings.csgo_db_url + self._settings.csgo_db_weapons_url,
            retry_options=self._retry_options,
        ) as response:
            return await response.json()

    async def get_skin_names(self, weapon: str) -> List[str]:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            self._settings.csgo_db_url + self._settings.csgo_db_skins_url.format(weapon=weapon),
            retry_options=self._retry_options,
        ) as response:
            return await response.json()

    async def get_csm_wiki_skin_data(self, weapon: str, skin: str):
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            self._settings.csm_wiki_url.format(weapon=weapon, skin=skin),
            retry_options=self._retry_options,
        ) as response:
            return await response.json()
