import json
from typing import Any, Dict

from tg_bot_float_steam_source.services.abstact_steam_source_service import (
    AbstractSteamSourceService,
)
from tg_bot_float_steam_source.services.dtos.cs_float_response_dto import CsFloatResponseDTO
from tg_bot_float_steam_source.services.dtos.steam_item_dto import SteamItemDTO
from tg_bot_float_steam_source.services.dtos.data_from_steam import DataFromSteam
from tg_bot_float_steam_source.services.dtos.cs_float_item_info_dto import CsFloatItemInfoDTO


class SteamFloatSourceService(AbstractSteamSourceService):
    @property
    def _headers(self) -> Dict[str, Any]:
        headers = super()._headers
        headers.update(json.loads(self._settings.steam_float_source_headers))
        return headers

    async def _get_response(self, link: str) -> CsFloatResponseDTO:
        response_json = await super()._get_response(link)
        return CsFloatResponseDTO.model_validate(response_json)

    async def get_steam_item(self, steam_response_dto: DataFromSteam) -> SteamItemDTO:
        link = self._settings.float_info_url.format(
            inspect_link=steam_response_dto.inspect_skin_link
        )
        cs_float_response = await self._get_response(link)
        return self._get_steam_item(cs_float_response, steam_response_dto)

    def _get_steam_item(
        self, cs_float_response_dto: CsFloatResponseDTO, data_from_steam_dto: DataFromSteam
    ) -> SteamItemDTO:
        item_info_dto = CsFloatItemInfoDTO.model_validate(cs_float_response_dto.iteminfo)
        return SteamItemDTO(
            name=item_info_dto.full_item_name,
            item_float=item_info_dto.floatvalue,
            price=data_from_steam_dto.price,
            buy_link=data_from_steam_dto.buy_link,
        )
