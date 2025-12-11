from fastapi import APIRouter

from tg_bot_float_common_dtos.csgo_db_source_dtos.additional_info_page_dto import (
    AdditionalInfoPageDTO,
)
from tg_bot_float_common_dtos.csgo_db_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_csgo_db_source.dependencies.page_services import (
    ADDITIONAL_INFO_PAGE_SERVICE,
    AGENTS_PAGE_SERVICE,
    GLOVES_PAGE_SERVICE,
    SKINS_PAGE_SERVICE,
    WEAPON_PAGE_SERVICE,
)
from tg_bot_float_csgo_db_source.dependencies.settings import REQUEST_SETTINGS
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController


class CsgoDBRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter()
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/weapons", self._get_weapons_page, methods=["GET"], response_model=WeaponsPageDTO
        )
        self._router.add_api_route(
            "/{weapon}/skins",
            self._get_skins_page,
            methods=["GET"],
            response_model=SkinsPageDTO,
        )
        self._router.add_api_route(
            "/{weapon}/{skin}",
            self._get_additional_info_page,
            methods=["GET"],
            response_model=AdditionalInfoPageDTO,
        )
        self._router.add_api_route(
            "/gloves",
            self._get_gloves_page,
            methods=["GET"],
            response_model=GlovesPageDTO,
        )
        self._router.add_api_route(
            "/agents",
            self._get_agents_page,
            methods=["GET"],
            response_model=AgentsPageDTO,
        )

    async def _get_weapons_page(
        self, service: WEAPON_PAGE_SERVICE, req_settings: REQUEST_SETTINGS
    ) -> WeaponsPageDTO:
        return await service.get_page(req_settings.base_domen + req_settings.weapons_path_url)

    async def _get_skins_page(
        self, weapon: str, service: SKINS_PAGE_SERVICE, req_settings: REQUEST_SETTINGS
    ) -> SkinsPageDTO:
        url = req_settings.base_domen + req_settings.skins_path_url.format(
            weapon=weapon.lower().replace("★ ", "").replace(" ", "-")
        )
        return await service.get_page(url)

    async def _get_additional_info_page(
        self,
        weapon: str,
        skin: str,
        service: ADDITIONAL_INFO_PAGE_SERVICE,
        req_settings: REQUEST_SETTINGS,
    ) -> AdditionalInfoPageDTO:
        return await service.get_page(
            req_settings.base_domen
            + req_settings.additional_info_path_url.format(
                name=weapon.lower().replace(" ", "-"),
                skin=skin.lower().replace(" ", "-"),
            )
        )

    async def _get_gloves_page(
        self, service: GLOVES_PAGE_SERVICE, req_settings: REQUEST_SETTINGS
    ) -> GlovesPageDTO:
        return await service.get_page(req_settings.base_domen + req_settings.gloves_path_url)

    async def _get_agents_page(
        self, service: AGENTS_PAGE_SERVICE, req_settings: REQUEST_SETTINGS
    ) -> AgentsPageDTO:
        return await service.get_page(req_settings.base_domen + req_settings.agents_path_url)
