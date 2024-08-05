import json
from typing import Any, Dict, List


from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO
from tg_bot_float_steam_source.services.abstact_steam_source_service import (
    AbstractSteamSourceService,
)
from tg_bot_float_steam_source.services.dtos.steam_response_dto import SteamResponseDTO
from tg_bot_float_steam_source.services.steam_source_exceptions import (
    IncorrectDataException,
    TooManyRequestsException,
)
from tg_bot_float_steam_source.services.dtos.data_from_steam import DataFromSteam
from tg_bot_float_steam_source.services.dtos.listing_info_dto import ListingInfoDTO
from tg_bot_float_steam_source.services.dtos.asset_info_dto import AssetInfoDTO
from tg_bot_float_steam_source.steam_source_constants import REQUESTS_ERROR_MSG, SKIN_DATA_ERROR_MSG


class SteamMarketSourceService(AbstractSteamSourceService):
    @property
    def _headers(self) -> Dict[str, Any]:
        headers = super()._headers
        headers.update(json.loads(self._settings.steam_market_source_headers))
        return headers

    async def _get_response(self, link: str) -> SteamResponseDTO:
        response_json = await super()._get_response(link)
        return SteamResponseDTO.model_validate(response_json)

    async def get_steam_response_dtos(
        self,
        item_request_dto: ItemRequestDTO,
        *,
        start: int = 0,
        count: int = 10,
        currency: int = 1,
    ) -> List[DataFromSteam]:
        link = self._get_valid_link(item_request_dto, start, count, currency)
        steam_response_dto = await self._get_response(link)
        self._check_on_errors(steam_response_dto)
        return self._find_items_from_steam_response(steam_response_dto, item_request_dto)

    def _get_valid_link(
        self, item_request_dto: ItemRequestDTO, start: int, count: int, currency: int
    ) -> str:
        market_link = self._get_market_link(item_request_dto)
        return (
            market_link
            + self._settings.render
            + self._settings.params.format(currency=currency, start=start, count=count)
        )

    def _get_market_link(self, item_request_dto: ItemRequestDTO) -> str:
        weapon = item_request_dto.weapon.replace(" ", "%20")
        skin = item_request_dto.skin.replace(" ", "%20")
        quality = item_request_dto.quality.replace(" ", "%20")
        stattrak = "StatTrak\u2122%20" if item_request_dto.stattrak else ""
        return self._settings.base_url + self._settings.item_url.format(
            weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
        )

    def _find_items_from_steam_response(
        self, steam_response_dto: SteamResponseDTO, item_request_dto: ItemRequestDTO
    ):
        items: List[DataFromSteam] = []
        for item in steam_response_dto.listinginfo.values():
            listing_info_dto = ListingInfoDTO.model_validate(item)
            asset_info_dto = AssetInfoDTO.model_validate(listing_info_dto.asset)
            inspect_link = self._get_inpect_link(asset_info_dto, listing_info_dto)
            buy_link = self._get_buy_link(item_request_dto, asset_info_dto, listing_info_dto)
            price = self._get_price(listing_info_dto)
            items.append(
                DataFromSteam(buy_link=buy_link, inspect_skin_link=inspect_link, price=float(price))
            )
        return items

    def _get_inpect_link(self, asset_info_dto: AssetInfoDTO, listing_info_dto: ListingInfoDTO):
        return (
            asset_info_dto.market_actions[0]["link"]
            .replace("%listingid%", listing_info_dto.listingid)
            .replace("%assetid%", asset_info_dto.id)
        )

    def _get_buy_link(
        self,
        item_request_dto: ItemRequestDTO,
        asset_info_dto: AssetInfoDTO,
        listing_info_dto: ListingInfoDTO,
    ):
        return self._get_market_link(item_request_dto) + self._settings.item_buy_url.format(
            listing_id=listing_info_dto.listingid,
            app_id=asset_info_dto.appid,
            context_id=asset_info_dto.contextid,
            asset_id=asset_info_dto.id,
        )

    def _get_price(self, listing_info_dto: ListingInfoDTO):
        price = str(
            listing_info_dto.converted_price_per_unit + listing_info_dto.converted_fee_per_unit
        )
        price = price[0:-2] + "." + price[-2:]
        return price

    def _check_on_errors(self, steam_response_dto: SteamResponseDTO) -> None:
        if not steam_response_dto.success:
            raise IncorrectDataException(SKIN_DATA_ERROR_MSG)
        if not steam_response_dto.listinginfo:
            raise TooManyRequestsException(REQUESTS_ERROR_MSG)
