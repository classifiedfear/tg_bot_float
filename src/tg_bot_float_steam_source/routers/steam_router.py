from typing import List
from fastapi import APIRouter

from tg_bot_float_steam_source.dependencies.services import STEAM_SOURCE_SERVICE
from tg_bot_float_steam_source.services.dtos.steam_item_response_dto import SteamItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO


class SteamRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/{weapon}/{skin}/{quality}/{stattrak}",
            self._get_steam_skin_data,
            methods=["GET"],
        )

    async def _get_steam_skin_data(
        self,
        steam_source_service: STEAM_SOURCE_SERVICE,
        weapon: str,
        skin: str,
        quality: str,
        stattrak: bool,
        start: int = 0,
        count: int = 10,
        currency: int = 1,
    ) -> List[SteamItemResponseDTO]:
        return await steam_source_service.get_steam_items(
            ItemRequestDTO(weapon=weapon, skin=skin, quality=quality, stattrak=stattrak),
            start=start,
            count=count,
            currency=currency,
        )
