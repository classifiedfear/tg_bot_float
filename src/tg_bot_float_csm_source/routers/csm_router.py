from typing import List
from fastapi import APIRouter
from tg_bot_float_csm_source.dependencies.params import GET_CSM_SKIN_DATA_PARAMS
from tg_bot_float_csm_source.dependencies.services import CSM_SERVICE
from tg_bot_float_csm_source.services.dtos.csm_item_response_dto import CsmItemDTO
from tg_bot_float_common_dtos.source_dtos.item_request_dto import ItemRequestDTO


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
            self._get_csm_skin_data,
            methods=["GET"],
        )

    async def _get_csm_skin_data(
        self, csm_service: CSM_SERVICE, path_params: GET_CSM_SKIN_DATA_PARAMS
    ) -> List[CsmItemDTO]:
        return await csm_service.get_csm_items(
            ItemRequestDTO(
                path_params.weapon, path_params.skin, path_params.quality, path_params.stattrak
            ),
            offset=path_params.offset,
        )
