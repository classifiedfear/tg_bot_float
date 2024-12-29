from typing import List

from fastapi import FastAPI

from tg_bot_float_misc.router_controller.abstract_router_controller import (
    AbstractRouterController,
)
from tg_bot_float_db_updater.router_controllers.db_updater_router_controller import (
    DbUpdaterRouterController,
)


router_controllers: List[AbstractRouterController] = [DbUpdaterRouterController()]

app = FastAPI()

for controller in router_controllers:
    app.include_router(controller.router)
