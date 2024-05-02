from fastapi import APIRouter, Request

from tg_bot_float_db_app.database.services.bot_db_refresher_service import BotDBRefresherService
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO
from tg_bot_float_db_app.api.dependencies.service_factory import DbServiceFactory

DB_ROUTER = APIRouter(prefix="/db", tags=["db"])

class ApiDBRouting:
    @DB_ROUTER.post("/update_db")
    async def update_db(
        self,
        request: Request,
        service_factory: DbServiceFactory) -> MsgResponseDTO:
        db_service = BotDBRefresherService(service_factory)
        try:
            await db_service.update(await request.body())
        except Exception as exp:
            return MsgResponseDTO(status=False, msg=repr(exp))
        return MsgResponseDTO(
            status=True,
            msg="Weapons, skins, qualities in the database were successfully updated."
            )


