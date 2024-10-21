from typing import List
from fastapi import FastAPI

from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_db_updater.router_controllers.db_data_updater_router import (
    DbDataUpdaterRouterController,
)


routers: List[AbstractRouterController] = [DbDataUpdaterRouterController()]

app = FastAPI()

for router in routers:
    app.include_router(router.router)
