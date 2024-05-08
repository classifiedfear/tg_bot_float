from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base


class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    weapon_id: Mapped[int] = mapped_column(Integer, nullable=True)

    skin_id: Mapped[int] = mapped_column(Integer, nullable=True)

    quality_id: Mapped[int] = mapped_column(Integer, nullable=True)

    stattrak: Mapped[bool] = mapped_column(Boolean, nullable=True)

    #user = relationship("UserModel", back_populates="subscriptions")
