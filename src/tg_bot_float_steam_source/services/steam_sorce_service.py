import asyncio
from typing import List
from aiohttp import ClientSession

from tg_bot_float_steam_source.services.steam_float_source_service import SteamFloatSourceService
from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO
from tg_bot_float_steam_source.services.steam_market_source_service import SteamMarketSourceService


class SteamSourceService:
    async def get_steam_items(
        self,
        weapon: str,
        skin: str,
        quality: str,
        stattrak: bool,
        *,
        start: int = 0,
        count: int = 10,
        currency: int = 1
    ) -> List[SteamItemResponseDTO]:
        async with ClientSession() as session:
            tasks = []
            steam_market_source_service = SteamMarketSourceService(session)
            steam_float_source_service = SteamFloatSourceService(session)
            steam_response_dtos = await steam_market_source_service.get_steam_response_dtos(
                weapon, skin, quality, stattrak, start=start, count=count, currency=currency
            )
            for response_dto in steam_response_dtos:
                task = asyncio.create_task(steam_float_source_service.get_steam_item(response_dto))
                tasks.append(task)
            return list(await asyncio.gather(*tasks))
