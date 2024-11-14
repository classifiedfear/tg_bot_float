from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.skin_model import SkinModel
else:
    SkinModel = "SkinModel"


class GloveModel(Base):
    __tablename__ = "glove"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    skins: Mapped[List[SkinModel]] = relationship(SkinModel, back_populates="glove")
