from typing import Any, Dict, List, Self

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings


class DbSourceDataGetterService:
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(self, settings: DbUpdaterSettings) -> None:
        self._settings = settings

    async def __aenter__(self) -> Self:
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    async def get_weapon_names(self) -> List[str]:
        return await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_weapons_url
        )

    async def get_skin_names(self, weapon: str) -> List[str]:
        return await self._get_response(
            self._settings.csgo_db_url + self._settings.csgo_db_skins_url.format(weapon=weapon)
        )

    async def get_csm_wiki_skin_data(self, weapon: str, skin: str) -> Dict[str, Any]:
        return await self._get_response(
            self._settings.csm_wiki_url.format(weapon=weapon, skin=skin)
        )

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            link,
            retry_options=self._retry_options,
        ) as response:
            return await response.json()
