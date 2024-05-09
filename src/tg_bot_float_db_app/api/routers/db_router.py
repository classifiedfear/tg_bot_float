from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from tg_bot_float_db_app.database.services.bot_db_refresher_service import BotDBRefresherService
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
    ) -> JSONResponse:
        async with service_factory:
            weapon_service = service_factory.get_weapon_service()
            skin_service = service_factory.get_skin_service()
            quality_service = service_factory.get_quality_service()
            relation_service = service_factory.get_relation_service()
            db_service = BotDBRefresherService(
                weapon_service, skin_service, quality_service, relation_service
            )
            await db_service.update(await request.body())
            return JSONResponse(content={"message": "DB successfully updated!"})
