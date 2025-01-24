from typing import List
from fastapi import FastAPI

from tg_bot_float_misc.router_controller.abstact_router_controller import AbstractRouterController
from tg_bot_float_steam_source.router_controllers.steam_router_controller import (
    SteamRouterController,
)
from tg_bot_float_steam_source.midlewares.error_handling_middleware import ErrorHandlingMiddleware

app = FastAPI()

router_controllers: List[AbstractRouterController] = [SteamRouterController()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for controller in router_controllers:
    app.include_router(controller.router)
