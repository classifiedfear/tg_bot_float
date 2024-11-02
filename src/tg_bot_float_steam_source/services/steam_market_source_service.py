import json
from typing import Any, Dict, List


from tg_bot_float_steam_source.router_controllers.steam_router_params.steam_params import (
    SteamParams,
)
from tg_bot_float_steam_source.services.abstact_source_service import (
    AbstractSourceService,
)
from tg_bot_float_steam_source.services.dtos.unprocessed_steam_response_dto import (
    UnprocessedSteamResponseDTO,
)
from tg_bot_float_steam_source.services.steam_source_exceptions import SteamSourceException
from tg_bot_float_steam_source.services.dtos.steam_market_response_dto import SteamMarketResponseDTO
from tg_bot_float_steam_source.services.dtos.listing_info_dto import ListingInfoDTO
from tg_bot_float_steam_source.services.dtos.asset_info_dto import AssetInfoDTO
from tg_bot_float_steam_source.steam_source_constants import STEAM_SOURCE_ERROR_MSG


class SteamMarketSourceService(AbstractSourceService):
    @property
    def _headers(self) -> Dict[str, Any]:
        headers = super()._headers
        headers.update(json.loads(self._settings.steam_market_source_headers))
        return headers

    async def _get_response(self, link: str) -> UnprocessedSteamResponseDTO:
        response_json = await super()._get_response(link)
        return UnprocessedSteamResponseDTO.model_validate(response_json)

    async def get_steam_market_response_dtos(
        self, steam_params: SteamParams
    ) -> List[SteamMarketResponseDTO]:
        link = self._get_market_json_link(steam_params)
        unprocessed_steam_response_dto = await self._get_response(link)
        self._check_on_errors(unprocessed_steam_response_dto)
        return self._get_processed_steam_market_response_dtos(
            unprocessed_steam_response_dto, steam_params
        )

    def _get_market_json_link(self, steam_params: SteamParams) -> str:
        market_link = self._get_market_link(steam_params)
        return (
            market_link
            + self._settings.render
            + self._settings.params.format(
                currency=steam_params.currency, start=steam_params.start, count=steam_params.count
            )
        )

    def _get_market_link(self, steam_params: SteamParams) -> str:
        weapon = steam_params.weapon.replace(" ", "%20")
        skin = steam_params.skin.replace(" ", "%20")
        quality = steam_params.quality.replace(" ", "%20")
        stattrak = "StatTrak\u2122%20" if steam_params.stattrak else ""
        return self._settings.base_url + self._settings.item_url.format(
            weapon=weapon, skin=skin, quality=quality, stattrak=stattrak
        )

    def _get_processed_steam_market_response_dtos(
        self, unprocessed_steam_response_dto: UnprocessedSteamResponseDTO, steam_params: SteamParams
    ):
        items: List[SteamMarketResponseDTO] = []
        if isinstance(unprocessed_steam_response_dto.listinginfo, dict):
            for response_dto in unprocessed_steam_response_dto.listinginfo.values():
                listing_info_dto = ListingInfoDTO.model_validate(response_dto)
                asset_info_dto = AssetInfoDTO.model_validate(listing_info_dto.asset)
                inspect_link = self._get_inpect_link(asset_info_dto, listing_info_dto)
                buy_link = self._get_buy_link(steam_params, asset_info_dto, listing_info_dto)
                price = self._get_price(listing_info_dto)
                items.append(
                    SteamMarketResponseDTO(
                        buy_link=buy_link, inspect_skin_link=inspect_link, price=float(price)
                    )
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
        steam_params: SteamParams,
        asset_info_dto: AssetInfoDTO,
        listing_info_dto: ListingInfoDTO,
    ):
        return self._get_market_link(steam_params) + self._settings.item_buy_url.format(
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

    def _check_on_errors(self, steam_response_dto: UnprocessedSteamResponseDTO) -> None:
        if isinstance(steam_response_dto.listinginfo, list) or not steam_response_dto.success:
            raise SteamSourceException(STEAM_SOURCE_ERROR_MSG)
