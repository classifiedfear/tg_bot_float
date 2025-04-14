from typing import Any, AsyncGenerator, List
from fastapi import FastAPI
from redis.asyncio import Redis

from tg_bot_float_telegram_app.api.api_router_controllers.tg_router_controller import (
    TgRouterController,
)
from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.command_router_controller import (
    CommandRouterController,
)

from tg_bot_float_telegram_app.telegram.telegram_routers.add_subscription_router_controller import (
    AddSubscriptionRouterController,
)
from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_settings import get_tg_settings


TG_SETTINGS = get_tg_settings()
REDIS_STORAGE = Redis(host=TG_SETTINGS.redis_host_url)
TG_KEYBOARD = Keyboard()

tg_app = TgBotFloatApp(TG_SETTINGS, REDIS_STORAGE)
db_app_service_client = DBAppServiceClient(TG_SETTINGS)

fastapi_routers = [TgRouterController(TG_SETTINGS, TG_KEYBOARD, tg_app, db_app_service_client)]
tg_routers: List[AbstractTGRouterController] = [
    CommandRouterController(TG_KEYBOARD, REDIS_STORAGE, db_app_service_client),
    AddSubscriptionRouterController(TG_KEYBOARD, db_app_service_client),
]

for tg_router in tg_routers:
    tg_app.add_tg_router_controller(tg_router)


async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, Any]:
    await tg_app.start_bot()
    yield
    await tg_app.stop_bot()
    await REDIS_STORAGE.close()
    await db_app_service_client.close()


app = FastAPI(lifespan=lifespan)


for router in fastapi_routers:
    app.include_router(router.router)
