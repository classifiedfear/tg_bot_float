from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.quality_model import QualityModel
    from tg_bot_float_db_app.database.models.skin_model import SkinModel
    from tg_bot_float_db_app.database.models.weapon_model import WeaponModel
else:
    WeaponModel = "WeaponModel"
    SkinModel = "SkinModel"
    QualityModel = "QualityModel"


class RelationModel(Base):
    __tablename__ = "relations"

    weapon_id: Mapped[int] = mapped_column(
        ForeignKey("weapon.id", ondelete="cascade"), primary_key=True, nullable=False
    )
    skin_id: Mapped[int] = mapped_column(
        ForeignKey("skin.id", ondelete="cascade"), primary_key=True, nullable=False
    )
    quality_id: Mapped[int] = mapped_column(
        ForeignKey("quality.id", ondelete="cascade"), primary_key=True, nullable=False
    )

    weapon: Mapped[WeaponModel] = relationship(back_populates="relations")
    skin: Mapped[SkinModel] = relationship(back_populates="relations")
    quality: Mapped[QualityModel] = relationship(back_populates="relations")
