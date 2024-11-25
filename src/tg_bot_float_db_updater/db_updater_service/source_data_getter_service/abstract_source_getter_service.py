from abc import ABC
from typing import Any, Self

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_db_updater.db_updater_settings import DbUpdaterSettings


class AbstractSourceGetterService(ABC):
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(self, settings: DbUpdaterSettings, session: ClientSession) -> None:
        self._settings = settings
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        await self._session.close()

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            link,
            retry_options=self._retry_options,
        ) as response:
            return await response.json()
