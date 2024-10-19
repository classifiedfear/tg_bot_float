import json
from typing import Any, Dict

from tg_bot_float_steam_source.services.abstact_source_service import (
    AbstractSourceService,
)
from tg_bot_float_steam_source.services.dtos.cs_float_response_dto import CsFloatResponseDTO
from tg_bot_float_steam_source.services.dtos.float_item_info_dto import FloatItemInfoDTO


class FloatSourceService(AbstractSourceService):
    @property
    def _headers(self) -> Dict[str, Any]:
        headers = super()._headers
        headers.update(json.loads(self._settings.steam_float_source_headers))
        return headers

    async def _get_response(self, link: str) -> CsFloatResponseDTO:
        response_json = await super()._get_response(link)
        return CsFloatResponseDTO.model_validate(response_json)

    async def get_float_item_info_dto(self, inspect_link: str) -> FloatItemInfoDTO:
        link = self._settings.float_info_url.format(inspect_link=inspect_link)
        cs_float_response = await self._get_response(link)
        return FloatItemInfoDTO.model_validate(cs_float_response.iteminfo)
