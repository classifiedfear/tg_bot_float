import pickle
from typing import List, Self

from aiohttp import ClientSession
import brotli

from tg_bot_float_csm_steam_benefit_finder.csm_steam_benefit_finder_settings import (
    CsmSteamBenefitFinderSettings,
)
from tg_bot_float_csm_steam_benefit_finder.benefit_finder_service.item_with_benefit_dto import ItemWithBenefitDTO


class CsmSteamBenefitSenderService:
    def __init__(self, settings: CsmSteamBenefitFinderSettings, session: ClientSession):
        self._settings = settings
        self._session = session


    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    async def send(self, items_with_benefit_dto: List[ItemWithBenefitDTO]):
        bytes_items_with_benefit = pickle.dumps(items_with_benefit_dto)
        compressed_items_dto = brotli.compress(bytes_items_with_benefit)
        async with self._session.post(
            self._settings.send_to_user, data=compressed_items_dto
        ) as response:
            assert response.status == 200