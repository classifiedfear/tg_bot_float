from typing import List
from fastapi import APIRouter

from tg_bot_float_csm_source.dependencies.services import CSM_SERVICE
from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO


class CsmRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route(
            "/{weapon}/{skin}/{quality}/{stattrak}",
            self._get_csm_skin_data,
            methods=["GET"],
        )

    async def _get_csm_skin_data(
        self, csm_service: CSM_SERVICE, weapon: str, skin: str, quality: str, stattrak: bool
    ) -> List[CsmItemResponseDTO]:
        return await csm_service.get_csm_items(weapon, skin, quality, stattrak)
