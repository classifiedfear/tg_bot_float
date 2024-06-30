from fastapi import FastAPI

from tg_bot_float_db_updater.routers.db_data_updater_router import DbDataUpdaterRouter


routers = [DbDataUpdaterRouter()]

app = FastAPI()

for router in routers:
    app.include_router(router.router)
