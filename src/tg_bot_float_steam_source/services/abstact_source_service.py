from abc import ABC, abstractmethod
from typing import Dict, Any, Self, Set

from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient
from fake_useragent import UserAgent

from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings


class AbstractSourceService(ABC):

    def __init__(self, settings: SteamSourceSettings, session: ClientSession) -> None:
        self._settings = settings
        self._session = session
        statuses = self._configure_not_retry_statuses()
        self._retry_options = ExponentialRetry(statuses=statuses)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    def _configure_not_retry_statuses(self) -> Set[int]:
        not_retry_statuses_str = self._settings.not_retry_statuses.split(",")
        not_retry_statuses = set(range(200, 300))
        not_retry_statuses |= {int(x) for x in not_retry_statuses_str}
        statuses = {x for x in range(100, 600) if x not in not_retry_statuses}
        return statuses

    @property
    @abstractmethod
    def _headers(self) -> Dict[str, Any]:
        return {"user-agent": f"{UserAgent.random}"}

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            link, headers=self._headers, retry_options=self._retry_options
        ) as response:
            return await response.json()
