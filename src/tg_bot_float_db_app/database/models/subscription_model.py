from typing import TYPE_CHECKING

from sqlalchemy import Integer, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base
from tg_bot_float_db_app.database.models.quality_model import QualityModel
from tg_bot_float_db_app.database.models.skin_model import SkinModel

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.user_model import UserModel
    from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
else:
    UserModel = "UserModel"
    WeaponModel = "WeaponModel"


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )

    user: Mapped[UserModel] = relationship(back_populates="subscriptions")

    weapon_id: Mapped[int] = mapped_column(
        ForeignKey("weapon.id", ondelete="cascade"), nullable=True
    )

    weapon: Mapped[WeaponModel] = relationship(back_populates="subscriptions")

    skin_id: Mapped[int] = mapped_column(ForeignKey("skin.id", ondelete="cascade"), nullable=True)

    skin: Mapped[SkinModel] = relationship(back_populates="subscriptions")

    quality_id: Mapped[int] = mapped_column(
        ForeignKey("quality.id", ondelete="cascade"), nullable=True
    )

    quality: Mapped[QualityModel] = relationship(back_populates="subscriptions")

    stattrak: Mapped[bool] = mapped_column(Boolean, nullable=True)
