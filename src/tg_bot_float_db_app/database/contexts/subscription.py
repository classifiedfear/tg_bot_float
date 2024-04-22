import sqlalchemy

from tg_bot_float_db_app.database.models.user_models import SubscriptionModel



class SubscriptionContext:
    def method(self):
        select_stmt = sqlalchemy.select(SubscriptionModel).group_by(
            SubscriptionModel.weapon_id,
        )

    async def save_changes(self) -> None:
        await self._session.commit()
