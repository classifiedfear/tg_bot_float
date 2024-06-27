from abc import ABC, abstractmethod
from typing import Dict, Any

from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient
from fake_useragent import UserAgent

from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings


class AbstractSteamSourceService(ABC):

    def __init__(self, settings: SteamSourceSettings, session: ClientSession) -> None:
        self._settings = settings
        _statuses = {
            x for x in range(100, 600) if str(x) not in self._settings.not_retry_statuses.split(",")
        }
        self._retry_options = ExponentialRetry(statuses=_statuses)
        self._session = session

    @property
    @abstractmethod
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_response(self, link: str) -> Dict[str, Any]:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            link, headers=self._headers, retry_options=self._retry_options
        ) as response:
            return await response.json()
