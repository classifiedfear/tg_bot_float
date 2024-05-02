from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base


class RelationModel(Base):
    __tablename__ = 'relations'

    weapon_id: Mapped[int] = mapped_column(
        ForeignKey('weapon.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    skin_id: Mapped[int] = mapped_column(
        ForeignKey('skin.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    quality_id: Mapped[int] = mapped_column(
        ForeignKey('quality.id', ondelete='cascade'), primary_key=True, nullable=False
    )

    weapon = relationship('WeaponModel', back_populates='relations')
    skin = relationship('SkinModel', back_populates='relations')
    quality = relationship('QualityModel', back_populates='relations')