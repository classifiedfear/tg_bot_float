import fastapi

from tg_bot_float_db_app.services.bot_database_refresher import BotDatabaseRefresher
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.bot_database_context import BotDatabaseContext


update_db_router = fastapi.APIRouter(
    prefix="/services",
    tags=["services"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_context)]
)


@update_db_router.post("/update_db")
async def update_db(request: fastapi.Request, context: BotDatabaseContext = fastapi.Depends(db_dependencies.get_db_context)):
    db_service = BotDatabaseRefresher(context)
    await db_service.refresh(await request.body())



