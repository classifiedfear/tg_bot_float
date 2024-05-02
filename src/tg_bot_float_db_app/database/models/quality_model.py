from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

class QualityModel(Base):
    __tablename__ = 'quality'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    relations = relationship(
        'RelationModel', back_populates='quality', cascade='all, delete', passive_deletes=True
    )