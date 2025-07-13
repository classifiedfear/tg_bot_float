from typing import List
from fastapi import FastAPI

from tg_bot_float_csm_wiki_source.router_controllers.csm_wiki_router_controller import (
    CsmWikiRouterController,
)
from tg_bot_float_csm_wiki_source.middlewares.error_handling_middleware import (
    ErrorHandlingMiddleware,
)
from tg_bot_float_misc.router_controller.abstract_router_controller import AbstractRouterController

router_controllers: List[AbstractRouterController] = [CsmWikiRouterController()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for controller in router_controllers:
    app.include_router(controller.router)
