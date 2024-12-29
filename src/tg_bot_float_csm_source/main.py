from typing import List
from fastapi import FastAPI

from tg_bot_float_csm_source.router_controllers.csm_router_controller import CsmRouterController
from tg_bot_float_csm_source.middlewares.error_handling_middleware import ErrorHandlingMiddleware
from tg_bot_float_misc.router_controller.abstact_router_controller import AbstractRouterController

app = FastAPI()

router_controllers: List[AbstractRouterController] = [CsmRouterController()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for controller in router_controllers:
    app.include_router(controller.router)
