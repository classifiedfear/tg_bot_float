from fastapi import FastAPI

from tg_bot_float_sub_benefit_finder.routers.benefit_finder_router import BenefitFinderRouter


routers = [BenefitFinderRouter()]

app = FastAPI()

for router in routers:
    app.include_router(router.router)
