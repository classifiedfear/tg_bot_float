from fastapi import FastAPI

from tg_bot_float_csm_wiki_source.routers.csm_wiki_router import CsmWikiRouter
from tg_bot_float_csm_wiki_source.middlewares.error_handling_middleware import (
    ErrorHandlingMiddleware,
)

routers = [CsmWikiRouter()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for router in routers:
    app.include_router(router.router)
