from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel


class SubscriptionService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
