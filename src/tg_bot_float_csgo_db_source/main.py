from typing import List
from fastapi import FastAPI

from tg_bot_float_csgo_db_source.router_controllers.csdb_router_controller import (
    CsgoDBRouterController,
)
from tg_bot_float_csgo_db_source.middlewares.error_handling_middleware import (
    ErrorHandlingMiddleware,
)
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController

router_controllers: List[AbstractRouterController] = [CsgoDBRouterController()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for controller in router_controllers:
    app.include_router(controller.router)
