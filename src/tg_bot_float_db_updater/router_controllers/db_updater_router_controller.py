from fastapi import APIRouter

from tg_bot_float_db_updater.dependencies.services import DB_UPDATER_SERVICE
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController


class DbUpdaterRouterController(AbstractRouterController):
    def __init__(self) -> None:
        self._router = APIRouter()
        super().__init__()

    def _init_routes(self) -> None:
        self._router.add_api_route("/update_db", self._update_db, methods=["GET"])

    async def _update_db(self, db_updater_service: DB_UPDATER_SERVICE) -> None:
        await db_updater_service.update()
