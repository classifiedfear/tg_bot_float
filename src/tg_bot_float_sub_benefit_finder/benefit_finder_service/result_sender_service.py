import pickle
from typing import List, Self

from aiohttp import ClientSession
import brotli

from tg_bot_float_sub_benefit_finder.sub_benefit_finder_settings import (
    CsmSteamBenefitFinderSettings,
)
from tg_bot_float_common_dtos.tg_result import TgResult


class ResultSenderService:
    def __init__(self, settings: CsmSteamBenefitFinderSettings, session: ClientSession):
        self._settings = settings
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    async def send(self, tg_result_dto: TgResult):
        bytes_tg_result = pickle.dumps(tg_result_dto)
        compressed_items_dto = brotli.compress(bytes_tg_result)
        async with self._session.post(
            self._settings.telegram_app_base_url + self._settings.send_update_url,
            data=compressed_items_dto,
        ) as response:
            assert response.status == 200
