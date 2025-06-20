from decimal import Decimal, localcontext
import json
from typing import Any, Dict, List, Self

from curl_cffi.requests import AsyncSession
from fake_useragent import UserAgent

from tg_bot_float_csm_source.csm_source_constants import NOT_EXIST_ERROR_MSG
from tg_bot_float_csm_source.csm_source_settings import CsmSourceSettings
from tg_bot_float_csm_source.router_controllers.csm_router_params.csm_params import CsmParams
from tg_bot_float_csm_source.services.dtos.csm_response_dto import CsmResponse
from tg_bot_float_csm_source.services.csm_source_exceptions import CsmSourceExceptions
from tg_bot_float_csm_source.services.dtos.csm_item_response_dto import CsmItemResponseDTO
from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO


class CsmService:
    def __init__(self, settings: CsmSourceSettings) -> None:
        self._settings = settings

    async def __aenter__(self) -> Self:
        self._session = AsyncSession()
        return self

    async def __aexit__(self, type, exc, traceback) -> None:
        await self._session.close()

    @property
    def _headers(self) -> Dict[str, Any]:
        headers = json.loads(self._settings.headers)
        headers["user-agent"] = f"{UserAgent.random}"
        return headers

    async def get_items_from_page(self, csm_params: CsmParams) -> List[CsmItemDTO]:
        """Parse 1 page from csm source"""
        link = self._get_valid_link(csm_params)
        csm_response = await self._get_csm_response(link)
        self._check_on_errors(csm_response)
        items = self._get_csm_items_from_response(csm_response)
        if not items:
            raise CsmSourceExceptions(NOT_EXIST_ERROR_MSG)
        return items

    def _get_valid_link(self, csm_params: CsmParams) -> str:
        weapon = csm_params.weapon.replace(" ", "%20")
        skin = csm_params.skin.replace(" ", "%20")
        quality_index = (
            csm_params.quality.find("-")
            if "-" in csm_params.quality
            else csm_params.quality.find(" ")
        )
        quality = csm_params.quality[0] + csm_params.quality[quality_index + 1]
        stattrak = "true" if csm_params.stattrak else "false"
        return self._settings.base_url + self._settings.params.format(
            weapon=weapon,
            skin=skin,
            quality=quality.lower(),
            stattrak=stattrak,
            offset=csm_params.offset,
        )

    async def _get_csm_response(self, link: str) -> CsmResponse:
        response = await self._session.get(link, headers=self._headers)
        json_response = response.json()
        return CsmResponse.model_validate(json_response)

    @staticmethod
    def _check_on_errors(csm_response: CsmResponse) -> None:
        if csm_response.error:
            raise CsmSourceExceptions(NOT_EXIST_ERROR_MSG)

    def _get_csm_items_from_response(self, csm_response: CsmResponse) -> List[CsmItemDTO]:
        csm_items: List[CsmItemDTO] = []
        for item in csm_response.items:
            item_response_dto = CsmItemResponseDTO.model_validate(item)
            if item_response_dto.overpay and (
                overpay_float := item_response_dto.overpay.get("float")
            ):
                csm_skin_response_dto = self._get_csm_item_dto(item_response_dto, overpay_float)
                csm_items.append(csm_skin_response_dto)
        return csm_items

    def _get_csm_item_dto(self, item: CsmItemResponseDTO, overpay_float: str) -> CsmItemDTO:
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
