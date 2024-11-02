from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tg_bot_float_csm_source.csm_source_constants import NOT_EXIST_ERROR_MSG
from tg_bot_float_csm_source.dependencies.params import CSM_PARAMS
from tg_bot_float_csm_source.dependencies.services import CSM_SERVICE
from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO


class CsmRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/{weapon}/{skin}/{quality}/{stattrak}",
            self._get_csm_items,
            methods=["GET"],
            response_model=None,
        )

    async def _get_csm_items(
        self, csm_service: CSM_SERVICE, csm_params: CSM_PARAMS
    ) -> List[CsmItemDTO] | JSONResponse:
        return await csm_service.get_items_from_page(csm_params)
