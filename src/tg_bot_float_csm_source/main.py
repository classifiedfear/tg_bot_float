from fastapi import FastAPI

from tg_bot_float_csm_source.routers.csm_router import CsmRouter
from tg_bot_float_csm_source.middlewares.error_handling_middleware import ErrorHandlingMiddleware

app = FastAPI()

routers = [CsmRouter()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)

for router in routers:
    app.include_router(router.router)
