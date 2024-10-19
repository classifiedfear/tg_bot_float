from fastapi import FastAPI

from tg_bot_float_steam_source.routers.steam_router import SteamRouter
from tg_bot_float_steam_source.midlewares.error_handling_middleware import ErrorHandlingMiddleware

app = FastAPI()

routers = [SteamRouter()]

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)
for router in routers:
    app.include_router(router.router)
