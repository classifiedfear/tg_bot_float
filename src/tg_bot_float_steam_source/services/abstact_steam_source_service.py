from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Dict, Any

from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient

from settings.steam_source_settings import SteamSourceSettings


class AbstractSteamSourceService(ABC):
    _statuses = {
        x
        for x in range(100, 600)
        if x not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
    }
    _retry_options = ExponentialRetry(statuses=_statuses)
    _settings = SteamSourceSettings()

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    @property
    @abstractmethod
    def _headers(self) -> Dict[str, Any]:
        pass

    async def _get_response(self, link: str):
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            link, headers=self._headers, retry_options=self._retry_options
        ) as response:
            return await response.json()
