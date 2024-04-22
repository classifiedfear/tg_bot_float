import fastapi

from tg_bot_float_db_app.db_services.bot_database_refresher import BotDatabaseRefresher
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.bot_database_context import BotDatabaseContext


db_router = fastapi.APIRouter(
    prefix="/db",
    tags=["db"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_context)]
)


@db_router.post("/update_db")
async def update_db(request: fastapi.Request, context: BotDatabaseContext = fastapi.Depends(db_dependencies.get_db_context)):
    db_service = BotDatabaseRefresher(context)
    try:
        await db_service.update(await request.body())
    except Exception as exp:
        return {"status": False, "massage": exp}
    return {"status": True, "message": "Weapons, skins, qualities in database has successfully updated."}


