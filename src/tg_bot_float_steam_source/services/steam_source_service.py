import asyncio
from typing import List, Self
from aiohttp import ClientSession

from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO
from tg_bot_float_steam_source.services.steam_float_source_service import SteamFloatSourceService
from tg_bot_float_steam_source.services.dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_steam_source.services.steam_market_source_service import SteamMarketSourceService
from tg_bot_float_steam_source.steam_source_settings import SteamSourceSettings


class SteamSourceService:
    def __init__(self, settings: SteamSourceSettings) -> None:
        self._settings = settings

    async def __aenter__(self) -> Self:
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    async def get_steam_items(
        self,
        item_request_dto: ItemRequestDTO,
        *,
        start: int = 0,
        count: int = 10,
        currency: int = 1
    ) -> List[SteamItemDTO]:
        tasks = []
        steam_market_source_service = SteamMarketSourceService(self._settings, self._session)
        steam_float_source_service = SteamFloatSourceService(self._settings, self._session)
        data_from_steam_dtos = await steam_market_source_service.get_steam_response_dtos(
            item_request_dto, start=start, count=count, currency=currency
        )
        for response_dto in data_from_steam_dtos:
            task = asyncio.create_task(steam_float_source_service.get_steam_item(response_dto))
            tasks.append(task)
        return list(await asyncio.gather(*tasks))
