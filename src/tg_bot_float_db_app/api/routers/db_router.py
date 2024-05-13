from fastapi import APIRouter, Request

from tg_bot_float_db_app.api.dependencies.db_service_factory import BOT_DB_SERVICE_FACTORY


class DBRouter:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/db", tags=["db"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        self._router.add_api_route("/update_db", self._update_db, methods=["POST"])

    async def _update_db(
        self, request: Request, service_factory: BOT_DB_SERVICE_FACTORY
    ) -> None:
        async with service_factory:
            db_refresher_service = service_factory.get_db_refresher_service()
            await db_refresher_service.update(await request.body())
