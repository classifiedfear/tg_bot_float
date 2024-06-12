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

    async def _get_response(self, link: str) -> Any:
        retry_session = RetryClient(self._session)
        async with retry_session.get(link, retry_options=self._retry_options) as response:
            return await response.json()

    async def get_user_subscriptions(self) -> List[Dict[str, Any]]:
        return await self._get_response(self._settings.user_subscription_url)

    async def get_weapon_skin_quality_names(self, weapon_id: int, skin_id: int, quality_id: int):
        return await self._get_response(
            self._settings.weapon_skin_quality_names_url.format(
                weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
            )
        )

    async def get_csm_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[Dict[str, Any]]:
        return await self._get_response(
            self._settings.csm_base_url
            + self._settings.item_url.format(
                weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
            )
        )

    async def get_steam_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[Dict[str, Any]]:
        return await self._get_response(
            self._settings.steam_base_url
            + self._settings.item_url.format(
                weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
            )
        )
