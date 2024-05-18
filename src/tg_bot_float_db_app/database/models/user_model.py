import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import VARCHAR, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
else:
    SubscriptionModel = "SubscriptionModel"


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)

    username: Mapped[VARCHAR] = mapped_column(VARCHAR(32), unique=False, nullable=True)

    full_name: Mapped[VARCHAR] = mapped_column(VARCHAR(100), unique=False, nullable=True)

    reg_date: Mapped[Date] = mapped_column(Date, default=datetime.date.today())

    subscriptions: Mapped[List[SubscriptionModel]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"{self.username}: " f"reg_day:{self.reg_date}; " f"id-{self.id} "
