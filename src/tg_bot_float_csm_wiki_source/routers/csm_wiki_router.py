from fastapi import APIRouter

from tg_bot_float_csm_wiki_source.dependencies import CSM_WIKI_SKIN_SERVICE
from tg_bot_float_csm_wiki_source.services.csm_wiki_skin_data_dto import CSMWikiSkinDataDTO

class CsmWikiRouter:
    def __init__(self):
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route(
            "/{weapon}/{skin}", self._get_csm_wiki_skin_data, methods=['GET']
            )

    async def _get_csm_wiki_skin_data(
        self, weapon: str, skin: str, csm_wiki_service: CSM_WIKI_SKIN_SERVICE
        ) -> CSMWikiSkinDataDTO:
        return await csm_wiki_service.get_csm_wiki_skin_data(weapon, skin)
