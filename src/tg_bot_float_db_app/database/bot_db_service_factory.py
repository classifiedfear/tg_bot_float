from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from tg_bot_float_db_app.database.services.agent_service import AgentService
from tg_bot_float_db_app.database.services.glove_service import GloveService
from tg_bot_float_db_app.database.services.weapon_service import WeaponService
from tg_bot_float_db_app.database.services.quality_service import QualityService
from tg_bot_float_db_app.database.services.skin_service import SkinService
from tg_bot_float_db_app.database.services.relation_service import RelationService
from tg_bot_float_db_app.database.services.user_service import UserService
from tg_bot_float_db_app.database.services.subscription_service import SubscriptionService
from tg_bot_float_db_app.database.services.bot_db_refresher_service import BotDBRefresherService


class BotDbServiceFactory:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine
        self._sessionmaker = async_sessionmaker(
            self._db_engine, expire_on_commit=False, autocommit=False
        )

    async def __aenter__(self):
        self._session = self._sessionmaker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()

    def get_weapon_service(self) -> WeaponService:
        return WeaponService(self._session)

    def get_skin_service(self) -> SkinService:
        return SkinService(self._session)

    def get_quality_service(self) -> QualityService:
        return QualityService(self._session)

    def get_glove_service(self) -> GloveService:
        return GloveService(self._session)

    def get_agent_service(self) -> AgentService:
        return AgentService(self._session)

    def get_user_service(self) -> UserService:
        return UserService(self._session)

    def get_subscription_service(self) -> SubscriptionService:
        return SubscriptionService(self._session)

    def get_relation_service(self) -> RelationService:
        return RelationService(self._session)

    def get_db_refresher_service(self) -> BotDBRefresherService:
        return BotDBRefresherService(self)
