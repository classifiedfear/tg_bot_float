import fastapi

from tg_bot_float_db_app.dependencies import db_dependencies

user_router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_context)]
)