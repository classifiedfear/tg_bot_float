from decimal import Decimal, localcontext
from typing import Any, Dict, List

from aiohttp import ClientSession
from fake_useragent import UserAgent

from settings.csm_source_settings import CsmSourceSettings
from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO
from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO
from tg_bot_float_csm_source.services.exceptions import CsmSourceExceptions


class CsmService:
    _settings = CsmSourceSettings()

    @property
    def _headers(self) -> Dict[str, Any]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,ru;q=0.9",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "user-agent": f"{UserAgent.random}",
        }

    async def get_csm_items(
        self, weapon: str, skin: str, quality: str, stattrak: bool, *, offset: int = 0
    ) -> List[CsmItemResponseDTO]:
        """Parse 1 page from csm_tests"""
        items: List[CsmItemResponseDTO] = []
        async with ClientSession() as session:
            print(self._get_valid_link(ItemRequestDTO(weapon, skin, quality, stattrak), offset))
            async with session.get(
                self._get_valid_link(ItemRequestDTO(weapon, skin, quality, stattrak), offset)
            ) as response:
                json_response = await response.json()
                if self._has_error(json_response):
                    raise CsmSourceExceptions(
                        "Items with this parameters does not exists in csm market!"
                    )
                for item in json_response["items"]:
                    if (overpay := item.get("overpay")) and (overpay_float := overpay.get("float")):
                        csm_skin_response_dto = self._get_csm_skin_response(item, overpay_float)
                        items.append(csm_skin_response_dto)
        return items

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

    @staticmethod
    def _has_error(json_response: Dict[str, Any]) -> bool:
        return "error" in json_response

    def _get_csm_skin_response(self, item: Dict[str, Any], overpay_float: str):
        item_name = item["fullName"]
        default_price = item["defaultPrice"]
        item_float = item["float"]
        default_price_with_float = self._get_default_price_with_float(
            default_price, float(overpay_float)
        )
        return CsmItemResponseDTO(
            name=item_name,
            item_float=float(item_float),
            price=default_price,
            price_with_float=default_price_with_float,
            overpay_float=float(overpay_float),
        )

    @staticmethod
    def _get_default_price_with_float(default_price: float, overpay_float: float) -> float:
        with localcontext() as context:
            context.prec = 4
            return float(Decimal(default_price + overpay_float) * 1)
