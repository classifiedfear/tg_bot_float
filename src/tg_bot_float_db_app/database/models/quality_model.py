from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.subscription_model import SubscriptionModel
    from tg_bot_float_db_app.database.models.relation_model import RelationModel
else:
    RelationModel = "RelationModel"
    SubscriptionModel = "SubscriptionModel"


class QualityModel(Base):
    __tablename__ = "quality"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    relations: Mapped[RelationModel] = relationship(
        back_populates="quality", cascade="all, delete", passive_deletes=True
    )

    subscriptions: Mapped[List[SubscriptionModel]] = relationship(back_populates="quality")
