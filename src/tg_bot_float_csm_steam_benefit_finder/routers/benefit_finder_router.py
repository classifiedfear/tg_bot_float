from fastapi import APIRouter

from tg_bot_float_csm_steam_benefit_finder.dependencies.services import (
    CSM_STEAM_BENEFIT_FINDER_SERVICE,
)


class BenefitFinderRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()
        self._subscriptions = []

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route(
            "/find_items_with_benefit", self._find_items_with_benefit, methods=["GET"]
        )

    async def _find_items_with_benefit(
        self, finder_service: CSM_STEAM_BENEFIT_FINDER_SERVICE
    ) -> None:
        await finder_service.find_items_with_benefit(self._subscriptions)
