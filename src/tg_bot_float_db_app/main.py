import fastapi


from tg_bot_float_db_app.routers.database import db_router
from tg_bot_float_db_app.routers.quality import quality_router
from tg_bot_float_db_app.routers.relation import relation_router
from tg_bot_float_db_app.routers.skin import skin_router
from tg_bot_float_db_app.routers.subscription import subscription_router
from tg_bot_float_db_app.routers.user import user_router
from tg_bot_float_db_app.routers.weapon import weapon_router

routers = [subscription_router, quality_router, skin_router, weapon_router, relation_router, db_router, user_router]

app = fastapi.FastAPI()
for router in routers:
    app.include_router(router)
