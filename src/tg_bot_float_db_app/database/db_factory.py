from sqlalchemy.ext import asyncio as async_alchemy

from tg_bot_float_db_app.database.bot_db_service_factory import BotDbServiceFactory
from tg_bot_float_db_app.database.bot_db_creator import BotDbCreator
from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
from tg_bot_float_db_app.database.models.glove_model import GloveModel
from tg_bot_float_db_app.database.models.agent_model import AgentModel
from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
from tg_bot_float_db_app.database.models.user_model import UserModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel
from tg_bot_float_db_app.database.models.relation_model import RelationModel
from tg_bot_float_db_app.db_settings import DBSettings


class BotDbFactory:
    _settings = DBSettings()  # type: ignore "Load settings for db_app_variables.env file"
    _engine = async_alchemy.create_async_engine(_settings.url, echo=True, pool_pre_ping=True)

    @staticmethod
    async def get_service_factory():
        return BotDbServiceFactory(BotDbFactory._engine)

    @staticmethod
    def get_db_creator():
        return BotDbCreator(BotDbFactory._engine)
