from typing import List
from fastapi import APIRouter

from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import (
    AgentsPageDTO,
)
from tg_bot_float_common_dtos.csgo_database_source_dtos.gloves_page_dto import (
    GlovesPageDTO,
)
from tg_bot_float_common_dtos.csgo_database_source_dtos.skins_page_dto import (
    SkinsPageDTO,
)
from tg_bot_float_common_dtos.csgo_database_source_dtos.weapons_page_dto import (
    WeaponsPageDTO,
)
from tg_bot_float_csgo_db_source.dependencies.services import (
    AGENT_PAGE_SERVICE,
    GLOVE_PAGE_SERVICE,
    WEAPON_PAGE_SERVICE,
    SKIN_PAGE_SERVICE,
)


class CsgoDBRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/weapons", self._get_weapons, methods=["GET"])
        self._router.add_api_route("/skins/{weapon}", self._get_skins, methods=["GET"])
        self._router.add_api_route("/gloves", self._get_gloves, methods=["GET"])
        self._router.add_api_route("/agents", self._get_agents, methods=["GET"])

    async def _get_weapons(
        self, weapon_page_service: WEAPON_PAGE_SERVICE
    ) -> WeaponsPageDTO:
        return await weapon_page_service.get_weapon_names()

    async def _get_skins(
        self, weapon: str, skin_page_service: SKIN_PAGE_SERVICE
    ) -> SkinsPageDTO:
        return await skin_page_service.get_skin_names(
            weapon.lower().replace(" ", "-").replace("★ ", "")
        )

    async def _get_gloves(
        self, glove_page_service: GLOVE_PAGE_SERVICE
    ) -> List[GlovesPageDTO]:
        return await glove_page_service.get_glove_names()

    async def _get_agents(
        self, agent_page_service: AGENT_PAGE_SERVICE
    ) -> List[AgentsPageDTO]:
        return await agent_page_service.get_agent_names()
