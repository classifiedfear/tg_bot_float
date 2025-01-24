from typing import Any

from aiohttp import ClientSession, ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from tg_bot_float_csm_steam_market_benefit_finder.csm_steam_market_benefit_finder_settings import (
    CsmSteamMarketBenefitFinderSettings,
)


class AbstractSourceDataGetter:
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(
        self, settings: CsmSteamMarketBenefitFinderSettings, session: ClientSession
    ) -> None:
        self._settings = settings
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(link, retry_options=self._retry_options) as response:
            return await response.json()
