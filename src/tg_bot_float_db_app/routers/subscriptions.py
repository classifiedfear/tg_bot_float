import fastapi

from tg_bot_float_db_app.dependencies import db_dependencies

subscription_router = fastapi.APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_context)]
)