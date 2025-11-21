from typing import List

from fastapi import FastAPI

from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController
from tg_bot_float_csm_steam_market_benefit_finder.router_controllers.benefit_finder_router import (
    BenefitFinderRouterController,
)


routers: List[AbstractRouterController] = [BenefitFinderRouterController()]

app = FastAPI()

for router in routers:
    app.include_router(router.router)
