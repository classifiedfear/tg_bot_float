from fastapi import FastAPI

from tg_bot_float_csgo_db_source.routers.csgo_db_router import CsgoDBRouter
from tg_bot_float_csgo_db_source.middlewares.error_handling_middleware import ErrorHandlingMiddleware

routers = [CsgoDBRouter()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)
for router in routers:
    app.include_router(router.router)
