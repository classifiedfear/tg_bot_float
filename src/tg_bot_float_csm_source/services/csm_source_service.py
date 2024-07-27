from decimal import Decimal, localcontext
import json
from typing import Any, Dict, List, Self

from aiohttp import ClientSession
from fake_useragent import UserAgent

from tg_bot_float_csm_source.csm_source_settings import CsmSourceSettings
from tg_bot_float_csm_source.services.dtos.csm_item_response_dto import CsmItemDTO
from tg_bot_float_csm_source.services.dtos.csm_response_dto import CsmResponse
from tg_bot_float_csm_source.services.csm_source_exceptions import CsmSourceExceptions
from tg_bot_float_csm_source.services.dtos.data_from_csm_item_dto import CsmItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO


class CsmService:
    def __init__(self, settings: CsmSourceSettings) -> None:
        self._settings = settings

    async def __aenter__(self) -> Self:
        self._session = ClientSession()
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    @property
    def _headers(self) -> Dict[str, Any]:
        headers = json.loads(self._settings.headers)
        headers["user-agent"] = f"{UserAgent.random}"
        return headers

    async def get_csm_items(
        self, item_request_dto: ItemRequestDTO, *, offset: int = 0
    ) -> List[CsmItemDTO]:
        """Parse 1 page from csm source"""
        csm_items: List[CsmItemDTO] = []
        link = self._get_valid_link(item_request_dto, offset)
        csm_response = await self._get_response(link)
        self._check_on_errors(csm_response)
        for item in csm_response.items:
            item_response_dto = CsmItemResponseDTO.model_validate(item)
            if item_response_dto.overpay and (
                overpay_float := item_response_dto.overpay.get("float")
            ):
                csm_skin_response_dto = self._get_csm_skin_response(
                    item_response_dto, overpay_float
                )
                csm_items.append(csm_skin_response_dto)
        return csm_items

    def _get_valid_link(self, item_dto: ItemRequestDTO, offset: int) -> str:
        weapon = item_dto.weapon.replace(" ", "%20")
        skin = item_dto.skin.replace(" ", "%20")
        quality_index = (
            item_dto.quality.find("-") if "-" in item_dto.quality else item_dto.quality.find(" ")
        )
        quality = item_dto.quality[0] + item_dto.quality[quality_index + 1]
        stattrak = "true" if item_dto.stattrak else "false"
        return self._settings.base_url + self._settings.params.format(
            weapon=weapon, skin=skin, quality=quality.lower(), stattrak=stattrak, offset=offset
        )

    async def _get_response(self, link: str) -> CsmResponse:
        async with self._session.get(link, headers=self._headers) as response:
            json_response = await response.json()
            return CsmResponse.model_validate(json_response)

    @staticmethod
    def _check_on_errors(csm_response: CsmResponse) -> None:
        if csm_response.error:
            raise CsmSourceExceptions("Items with this parameters does not exists in csm market!")

    def _get_csm_skin_response(self, item: CsmItemResponseDTO, overpay_float: str):
        default_price_with_float = self._get_default_price_with_float(
            item.defaultPrice, float(overpay_float)
        )
        return CsmItemDTO(
            name=item.fullName,
            item_float=float(item.float),
            price=item.defaultPrice,
            price_with_float=default_price_with_float,
            overpay_float=float(overpay_float),
        )

    @staticmethod
    def _get_default_price_with_float(default_price: float, overpay_float: float) -> float:
        with localcontext() as context:
            context.prec = 4
            return float(Decimal(default_price + overpay_float) * 1)
