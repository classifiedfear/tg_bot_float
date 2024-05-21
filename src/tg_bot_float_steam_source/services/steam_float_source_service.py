from typing import Any, Dict

from fake_useragent import UserAgent

from tg_bot_float_steam_source.services.abstact_steam_source_service import (
    AbstractSteamSourceService,
)
from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO
from tg_bot_float_steam_source.services.steam_response_dto import SteamResponseDTO


class SteamFloatSourceService(AbstractSteamSourceService):
    @property
    def _headers(self):
        return {"Origin": "https://csfloat.com", "user-agent": f"{UserAgent.random}"}

    async def get_steam_item(self, steam_response_dto: SteamResponseDTO) -> SteamItemResponseDTO:
        link = self._settings.float_info_url.format(
            inspect_link=steam_response_dto.inspect_skin_link
        )
        json_response = await self._get_response(link)
        return self._get_steam_item(json_response, steam_response_dto)

    def _get_steam_item(self, json_response: Dict[str, Any], steam_response_dto: SteamResponseDTO):
        item_info = json_response["iteminfo"]
        return SteamItemResponseDTO(
            name=item_info["full_item_name"],
            item_float=item_info["floatvalue"],
            price=steam_response_dto.price,
            buy_link=steam_response_dto.buy_link,
        )
