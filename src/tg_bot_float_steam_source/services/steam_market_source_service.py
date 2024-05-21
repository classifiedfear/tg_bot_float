from typing import Any, Dict, List
from http import HTTPStatus

from fake_useragent import UserAgent

from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO
from tg_bot_float_steam_source.services.abstact_steam_source_service import (
    AbstractSteamSourceService,
)
from tg_bot_float_steam_source.services.steam_source_exceptions import (
    IncorrectDataException,
    TooManyRequestsException,
)
from tg_bot_float_steam_source.services.steam_response_dto import SteamResponseDTO


class SteamMarketSourceService(AbstractSteamSourceService):
    @property
    def _headers(self) -> Dict[str, Any]:
        return {
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,ru;q=0.9",
            "Connection": "keep-alive",
            "Host": "steamcommunity.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Prototype-Version": "1.7",
            "X-Requested-With": "XMLHttpRequest",
            "user-agent": f"{UserAgent.random}",
        }

    def _get_valid_link(
        self, item_request_dto: ItemRequestDTO, start: int, count: int, currency: int
    ):
        market_link = self._get_market_link(item_request_dto)
        return (
            market_link
            + self._settings.render
            + self._settings.params.format(currency=currency, start=start, count=count)
        )

    def _get_market_link(self, item_request_dto: ItemRequestDTO):
        weapon = item_request_dto.weapon.replace(" ", "%20")
        skin = item_request_dto.skin.replace(" ", "%20")
        quality = item_request_dto.quality.replace(" ", "%20")
        stattrak = "StatTrak\u2122%20" if item_request_dto.stattrak else ""
        return self._settings.base_url + self._settings.item_url.format(
            weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
        )

    async def get_steam_response_dtos(
        self,
        weapon: str,
        skin: str,
        quality: str,
        stattrak: bool,
        *,
        start: int = 0,
        count: int = 10,
        currency: int = 1,
    ) -> List[SteamResponseDTO]:
        item_request_dto = ItemRequestDTO(weapon, skin, quality, stattrak)
        link = self._get_valid_link(item_request_dto, start, count, currency)
        print(link)
        json_response = await self._get_response(link)
        return self._find_items_from_steam_response(json_response, item_request_dto)

    def _find_items_from_steam_response(
        self, json_response: Dict[str, Any], item_request_dto: ItemRequestDTO
    ):
        items: List[SteamResponseDTO] = []
        listing_info = self._get_listing_info(json_response)
        for item in listing_info.values():
            asset = item["asset"]
            inspect_link = (
                asset["market_actions"][0]["link"]
                .replace("%listingid%", item["listingid"])
                .replace("%assetid%", asset["id"])
            )
            buy_link = self._get_market_link(item_request_dto) + self._settings.item_buy_url.format(
                listing_id=item["listingid"],
                app_id=asset["appid"],
                context_id=asset["contextid"],
                asset_id=asset["id"],
            )
            price = str(item["converted_price_per_unit"] + item["converted_fee_per_unit"])
            price = price[0:-2] + "." + price[-2:]
            items.append(
                SteamResponseDTO(
                    buy_link=buy_link, inspect_skin_link=inspect_link, price=float(price)
                )
            )
        return items

    def _get_listing_info(self, json_response: Dict[str, Any]) -> Dict[str, Any]:
        if not json_response["success"]:
            raise TooManyRequestsException(
                "Слишком много запросов. Попробуйте позже!"
            )
        if not (listing_info := json_response["listinginfo"]):
            raise IncorrectDataException(
                "Были неверно введенны данные!",
            )
        return listing_info
