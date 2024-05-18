from fastapi import FastAPI

from tg_bot_float_csgo_db_source.routers.csgo_db_router import CsgoDBRouter

routers = [CsgoDBRouter()]

app = FastAPI()
for router in routers:
    app.include_router(router.router)
