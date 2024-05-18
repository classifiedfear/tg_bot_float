from typing import List
from fastapi import APIRouter

from tg_bot_float_csgo_db_source.dependencies import WEAPON_PAGE_SERVICE, SKIN_PAGE_SERVICE

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

    async def _get_weapons(self, weapon_page_service: WEAPON_PAGE_SERVICE) -> List[str]:
        return await weapon_page_service.get_weapon_names()

    async def _get_skins(self, weapon: str, skin_page_service: SKIN_PAGE_SERVICE) -> List[str]:
        return await skin_page_service.get_skin_names(weapon)
