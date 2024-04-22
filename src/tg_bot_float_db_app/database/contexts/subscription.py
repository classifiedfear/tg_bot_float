import sqlalchemy

from tg_bot_float_db_app.database.models.user_models import SubscriptionModel
from tg_bot_float_db_app.database.contexts.interface import Table


class SubscriptionContext(Table):
    def method(self):
        select_stmt = sqlalchemy.select(SubscriptionModel).group_by(
            SubscriptionModel.weapon_id,
        )
