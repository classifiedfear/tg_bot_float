import fastapi

from tg_bot_float_db_app.database.db_factory import BotDbFactory

SUBSCRIPTION_ROUTER = fastapi.APIRouter(prefix="/subscriptions", tags=["subscriptions"])