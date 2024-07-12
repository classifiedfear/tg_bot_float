from typing import TYPE_CHECKING

from sqlalchemy import Integer, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.user_model import UserModel
else:
    UserModel = "UserModel"


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[BigInteger] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )

    weapon_id: Mapped[int] = mapped_column(
        ForeignKey("weapon.id", ondelete="cascade"), nullable=True
    )

    skin_id: Mapped[int] = mapped_column(ForeignKey("skin.id", ondelete="cascade"), nullable=True)

    quality_id: Mapped[int] = mapped_column(
        ForeignKey("quality.id", ondelete="cascade"), nullable=True
    )

    stattrak: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user: Mapped[UserModel] = relationship(back_populates="subscriptions")
