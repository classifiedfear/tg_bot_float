import fastapi


from tg_bot_float_db_app.routers.quality import quality_router
from tg_bot_float_db_app.routers.skins import skin_router
from tg_bot_float_db_app.routers.weapons import weapon_router
from tg_bot_float_db_app.routers.relation import relation_router
from tg_bot_float_db_app.routers.subscriptions import subscription_router
from tg_bot_float_db_app.routers.services import update_db_router
from tg_bot_float_db_app.routers.users import user_router

routers_ = [subscription_router, quality_router, skin_router, weapon_router, relation_router, update_db_router, user_router]

app = fastapi.FastAPI()
for router in routers_:
    app.include_router(router)
