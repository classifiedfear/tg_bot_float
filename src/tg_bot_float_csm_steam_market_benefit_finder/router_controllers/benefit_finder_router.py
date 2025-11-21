from fastapi import APIRouter

from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController
from tg_bot_float_csm_steam_market_benefit_finder.dependencies.services import (
    CSM_STEAM_MARKET_BENEFIT_FINDER_SERVICE,
)


class BenefitFinderRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter()
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/csm_steam_market_benefit", self._find_items_with_benefit, methods=["GET"]
        )

    async def _find_items_with_benefit(
        self, finder_service: CSM_STEAM_MARKET_BENEFIT_FINDER_SERVICE
    ) -> None:
        await finder_service.find_items_with_benefit()
