from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tg_bot_float_csm_source.dependencies.params import CSM_PARAMS
from tg_bot_float_csm_source.dependencies.services import CSM_SERVICE
from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_misc.router_controller.abstact_router_controller import AbstractRouterController


class CsmRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter()
        super().__init__()

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
