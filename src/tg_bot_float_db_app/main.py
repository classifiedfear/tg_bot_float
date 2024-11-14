from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from tg_bot_float_db_app.api.router_controllers.agent_router_controller import AgentRouterController
from tg_bot_float_db_app.api.router_controllers.glove_router_controller import GloveRouterController
from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_db_app.api.router_controllers.quality_router_controller import (
    QualityRouterController,
)
from tg_bot_float_db_app.api.router_controllers.relation_router_controller import (
    RelationRouterController,
)
from tg_bot_float_db_app.api.router_controllers.skin_router_controller import SkinRouterController
from tg_bot_float_db_app.api.router_controllers.subscription_router_controller import (
    SubscriptionRouter,
)
from tg_bot_float_db_app.api.router_controllers.user_router_controller import UserRouterController
from tg_bot_float_db_app.api.router_controllers.weapon_router_controller import (
    WeaponRouterController,
)
from tg_bot_float_db_app.database.db_factory import BotDbFactory
from tg_bot_float_db_app.middlewares.error_handling_middleware import ErrorHandlingMiddleware
from tg_bot_float_db_app.api.router_controllers.db_router_controller import DBRouterController

routers: List[AbstractRouterController] = [
    WeaponRouterController(),
    SkinRouterController(),
    QualityRouterController(),
    AgentRouterController(),
    GloveRouterController(),
    RelationRouterController(),
    DBRouterController(),
    UserRouterController(),
    SubscriptionRouter(),
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    db_creator = BotDbFactory.get_db_creator()
    await db_creator.create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(ErrorHandlingMiddleware)

for router in routers:
    app.include_router(router.router)

add_pagination(app)
