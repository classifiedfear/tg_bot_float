from sqlalchemy import BigInteger, Integer, Table, Column, ForeignKey

from tg_bot_float_db_app.database.models.base import Base

user_subscription = Table(
    'user_subscription', Base.metadata,
    Column('user_id', BigInteger, ForeignKey('user.id')),
    Column('subscription_id', Integer, ForeignKey('subscription.id'))
)
