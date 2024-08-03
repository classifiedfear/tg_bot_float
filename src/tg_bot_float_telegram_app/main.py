from fastapi import FastAPI

from tg_bot_float_telegram_app.api.api_router_controllers.tg_router_controller import (
    TgRouterController,
)
from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_settings import get_tg_settings


TG_SETTINGS = get_tg_settings()
tg_app = TgBotFloatApp(TG_SETTINGS)
routers = [TgRouterController(TG_SETTINGS, tg_app)]


app = FastAPI(lifespan=tg_app.start_bot)


for router in routers:
    app.include_router(router.router)
