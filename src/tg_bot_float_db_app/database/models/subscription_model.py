from typing import TYPE_CHECKING

from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.user_model import UserModel
else:
    UserModel = "UserModel"


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    weapon_id: Mapped[int] = mapped_column(Integer, nullable=True)

    skin_id: Mapped[int] = mapped_column(Integer, nullable=True)

    quality_id: Mapped[int] = mapped_column(Integer, nullable=True)

    stattrak: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user: Mapped[UserModel] = relationship(back_populates="subscriptions")
