from fastapi import APIRouter

from tg_bot_float_csm_wiki_source.dependencies.services import CSM_WIKI_SKIN_SERVICE
from tg_bot_float_common_dtos.csm_wiki_source_dtos.csm_wiki_dto import CsmWikiDTO
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController


class CsmWikiRouterController(AbstractRouterController):
    def __init__(self):
        self._router = APIRouter()
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/{weapon}/{skin}", self._get_csm_wiki_skin_data, methods=["GET"]
        )

    async def _get_csm_wiki_skin_data(
        self, weapon: str, skin: str, csm_wiki_service: CSM_WIKI_SKIN_SERVICE
    ) -> CsmWikiDTO:
        return await csm_wiki_service.get_weapon_skin_data(weapon, skin)
