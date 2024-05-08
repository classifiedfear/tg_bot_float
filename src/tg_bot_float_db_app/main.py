from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from tg_bot_float_db_app.api.routers.db_router import DBRouter
from tg_bot_float_db_app.api.routers.quality_router import QualityRouter
from tg_bot_float_db_app.api.routers.relation_router import RelationRouter
from tg_bot_float_db_app.api.routers.skin_router import SkinRouter
from tg_bot_float_db_app.api.routers.subscription_router import SubscriptionRouter
from tg_bot_float_db_app.api.routers.user_router import UserRouter
from tg_bot_float_db_app.api.routers.weapon_router import WeaponRouter
from tg_bot_float_db_app.database.db_factory import BotDbFactory

routers = [
    WeaponRouter(),
    SkinRouter(),
    QualityRouter(),
    RelationRouter(),
    DBRouter(),
    UserRouter(),
    SubscriptionRouter(),
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    db_creator = BotDbFactory.get_db_creator()
    await db_creator.create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router.router)
