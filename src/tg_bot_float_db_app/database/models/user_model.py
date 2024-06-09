from typing import List, TYPE_CHECKING

from sqlalchemy import VARCHAR, Date, BigInteger, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
else:
    SubscriptionModel = "SubscriptionModel"


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    username: Mapped[VARCHAR] = mapped_column(VARCHAR(32), unique=False, nullable=True)

    full_name: Mapped[VARCHAR] = mapped_column(VARCHAR(100), unique=False, nullable=True)

    reg_date: Mapped[Date] = mapped_column(Date, server_default=func.now())

    subscriptions: Mapped[List[SubscriptionModel]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"{self.username}: " f"reg_day:{self.reg_date}; " f"id-{self.id} "
