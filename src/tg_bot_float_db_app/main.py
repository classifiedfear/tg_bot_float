
from typing import Any, AsyncGenerator
from fastapi import FastAPI
from tg_bot_float_db_app.api.routers.db_router import DB_ROUTER
from tg_bot_float_db_app.api.routers.quality_router import QUALITY_ROUTER
from tg_bot_float_db_app.api.routers.relation_router import RELATION_ROUTER
from tg_bot_float_db_app.api.routers.skin_router import SKIN_ROUTER
from tg_bot_float_db_app.api.routers.subscription_router import SUBSCRIPTION_ROUTER
from tg_bot_float_db_app.api.routers.user_router import USER_ROUTER
from tg_bot_float_db_app.api.routers.weapon_router import WEAPON_ROUTER
from tg_bot_float_db_app.database.db_factory import BotDbFactory

routers = [
    SUBSCRIPTION_ROUTER, QUALITY_ROUTER, SKIN_ROUTER, WEAPON_ROUTER, RELATION_ROUTER, DB_ROUTER, USER_ROUTER
    ]

async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    db_creator = BotDbFactory.get_db_creator()
    await db_creator.create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)
for router in routers:
    app.include_router(router)
