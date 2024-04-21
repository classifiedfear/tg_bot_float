import sqlalchemy

from tg_bot_float_db_app.database.models import user_models
from tg_bot_float_db_app.database.tables.interface import Table


class SubscriptionTable(Table):
    def method(self):
        select_stmt = sqlalchemy.select(user_models.Subscription).group_by(
            user_models.Subscription.weapon_id,
        )
