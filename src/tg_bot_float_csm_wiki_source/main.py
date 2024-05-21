from fastapi import FastAPI

from tg_bot_float_csm_wiki_source.routers.csm_wiki_router import CsmWikiRouter

routers = [CsmWikiRouter()]

app = FastAPI()
for router in routers:
    app.include_router(router.router)
