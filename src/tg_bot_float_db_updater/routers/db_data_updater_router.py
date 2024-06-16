from fastapi import APIRouter

from tg_bot_float_db_updater.dependencies.services import DB_UPDATER_SERVICE

class DbDataUpdaterRouter:
    def __init__(self):
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/update_db", self._update_db, methods=["GET"])

    async def _update_db(self, db_updater_service: DB_UPDATER_SERVICE) -> None:
        await db_updater_service.update()
