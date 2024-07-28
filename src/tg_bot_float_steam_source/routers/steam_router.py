from typing import List
from fastapi import APIRouter

from tg_bot_float_steam_source.dependencies.params import GET_STEAM_SKIN_DATA_PARAMS
from tg_bot_float_steam_source.dependencies.services import STEAM_SOURCE_SERVICE
from tg_bot_float_steam_source.services.dtos.steam_item_dto import SteamItemDTO
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
        self, steam_source_service: STEAM_SOURCE_SERVICE, steam_params: GET_STEAM_SKIN_DATA_PARAMS
    ) -> List[SteamItemDTO]:
        return await steam_source_service.get_steam_items(
            ItemRequestDTO(
                weapon=steam_params.weapon,
                skin=steam_params.skin,
                quality=steam_params.quality,
                stattrak=steam_params.stattrak,
            ),
            start=steam_params.start,
            count=steam_params.count,
            currency=steam_params.currency,
        )
