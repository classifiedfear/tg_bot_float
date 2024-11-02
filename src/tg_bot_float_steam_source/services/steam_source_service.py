import asyncio
from typing import List

from tg_bot_float_steam_source.routers.steam_router_params.steam_params import SteamParams
from tg_bot_float_steam_source.services.dtos.steam_market_response_dto import SteamMarketResponseDTO
from tg_bot_float_steam_source.services.float_source_service import FloatSourceService
from tg_bot_float_steam_source.services.steam_market_source_service import SteamMarketSourceService
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO


class SteamSourceService:
    def __init__(
        self,
        steam_market_source_service: SteamMarketSourceService,
        float_source_service: FloatSourceService,
    ) -> None:

        self._steam_market_source_service = steam_market_source_service
        self._float_source_service = float_source_service

    async def get_steam_items(self, steam_params: SteamParams) -> List[SteamItemDTO]:
        tasks = []
        steam_market_response_dtos = (
            await self._steam_market_source_service.get_steam_market_response_dtos(steam_params)
        )
        for response_dto in steam_market_response_dtos:
            task = asyncio.create_task(self._get_steam_item_dto(response_dto))
            tasks.append(task)
        return list(await asyncio.gather(*tasks))

    async def _get_steam_item_dto(self, steam_response_dto: SteamMarketResponseDTO) -> SteamItemDTO:
        float_item_info_dto = await self._float_source_service.get_float_item_info_dto(
            steam_response_dto.inspect_skin_link
        )
        return SteamItemDTO(
            name=float_item_info_dto.full_item_name,
            item_float=float_item_info_dto.floatvalue,
            price=steam_response_dto.price,
            buy_link=steam_response_dto.buy_link,
        )
