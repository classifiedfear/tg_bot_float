import datetime

from sqlalchemy import VARCHAR, Date, BigInteger, Integer, Table, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from tg_bot_float_db_app.database.declar_base import Base


user_subscription = Table(
    'user_subscription', Base.metadata,
    Column('user_id', BigInteger, ForeignKey('user.id')),
    Column('subscription_id', Integer, ForeignKey('subscription.id'))
)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, primary_key=True
    )
    username: Mapped[VARCHAR] = mapped_column(
        VARCHAR(32), unique=False, nullable=True
    )
    full_name: Mapped[VARCHAR] = mapped_column(
        VARCHAR(100), unique=False, nullable=True
    )
    reg_date: Mapped[Date] = mapped_column(Date, default=datetime.date.today())

    def __repr__(self) -> str:
        return (f'{self.username}: '
                f'reg_day:{self.reg_date}; '
                f'id-{self.id} ')


class Subscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    weapon_id: Mapped[int] = mapped_column(Integer, nullable=True)

    skin_id: Mapped[int] = mapped_column(Integer, nullable=True)

    quality_id: Mapped[int] = mapped_column(Integer, nullable=True)

    stattrak: Mapped[bool] = mapped_column(Boolean, nullable=True)
