from typing import Any, Dict, List

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from aiohttp_retry import ExponentialRetry, RetryClient

from settings.csm_steam_benefit_finder_settings import CsmSteamBenefitFinderSettings


class SourceDataGetterService:
    _retry_options = ExponentialRetry(exceptions={ContentTypeError})

    def __init__(self, settings: CsmSteamBenefitFinderSettings) -> None:
        self._settings = settings

    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._session.close()

    async def get_item_to_find(self) -> Dict[str, Any]:
        # Unfinished, temporary solution
        return {"weapon": "AK-47", "skin": "Asiimov", "quality": "Field-Tested", "stattrak": False}

    async def get_csm_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[Dict[str, Any]]:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            self._settings.csm_base_url
            + self._settings.item_url.format(
                weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
            ),
            retry_options=self._retry_options,
        ) as response:
            return await response.json()

    async def get_steam_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[Dict[str, Any]]:
        retry_session = RetryClient(self._session)
        async with retry_session.get(
            self._settings.steam_base_url
            + self._settings.item_url.format(
                weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
            ),
            retry_options=self._retry_options,
        ) as response:
            return await response.json()
