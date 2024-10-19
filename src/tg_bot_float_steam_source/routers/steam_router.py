from typing import List
from fastapi import APIRouter

from tg_bot_float_steam_source.dependencies.params import STEAM_PARAMS
from tg_bot_float_steam_source.dependencies.services import STEAM_SOURCE_SERVICE
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO



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
        self, steam_source_service: STEAM_SOURCE_SERVICE, steam_params: STEAM_PARAMS
    ) -> List[SteamItemDTO]:
        return await steam_source_service.get_steam_items(steam_params)
