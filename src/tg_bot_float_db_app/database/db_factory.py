from sqlalchemy.ext import asyncio as async_alchemy

from tg_bot_float_db_app.database.bot_db_service_factory import BotDbServiceFactory
from tg_bot_float_db_app.database.bot_db_creator import BotDbCreator
from settings import DB_SETTINGS


class BotDbFactory:
    _engine = async_alchemy.create_async_engine(DB_SETTINGS.url, echo=True, pool_pre_ping=True)

    @staticmethod
    async def get_service_factory():
        return BotDbServiceFactory(BotDbFactory._engine)

    @staticmethod
    def get_db_creator():
        return BotDbCreator(BotDbFactory._engine)
