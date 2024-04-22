from sqlalchemy.ext import asyncio as async_alchemy

from tg_bot_float_db_app.database.bot_database_engine import BotDatabaseEngine
from tg_bot_float_db_app.database.contexts.weapon import WeaponContext
from tg_bot_float_db_app.database.contexts.quality import QualityContext
from tg_bot_float_db_app.database.contexts.skin import SkinContext
from tg_bot_float_db_app.database.contexts.relation import RelationsContext
from tg_bot_float_db_app.database.contexts.user import UserContext
from tg_bot_float_db_app.database.contexts.subscription import SubscriptionContext

class BotDatabaseContext:
    def __init__(self, db_engine: BotDatabaseEngine):
        self._db_engine = db_engine
        self._session_maker = async_alchemy.async_sessionmaker(
            self._db_engine.engine, expire_on_commit=False, autocommit=False
        )

    async def __aenter__(self):
        await self._db_engine.create_all_tables()
        self._session = self._session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()

    def get_weapon_context(self) -> WeaponContext:
        return WeaponContext(self._session)

    def get_skin_context(self) -> SkinContext:
        return SkinContext(self._session)

    def get_quality_context(self) -> QualityContext:
        return QualityContext(self._session)

    def get_user_context(self) -> UserContext:
        return UserContext(self._session)

    def get_subscription_context(self) -> SubscriptionContext:
        return SubscriptionContext(self._session)

    def get_weapon_skin_quality_table(self) -> RelationsContext:
        return RelationsContext(self._session)
