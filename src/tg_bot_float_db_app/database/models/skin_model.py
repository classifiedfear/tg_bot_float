from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

class SkinModel(Base):
    __tablename__ = 'skin'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    stattrak_existence: Mapped[bool] = mapped_column(Boolean, nullable=False)

    relations = relationship(
        'RelationModel', back_populates='skin', cascade='all, delete', passive_deletes=True
    )