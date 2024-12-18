from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg_bot_float_db_app.database.models.base import Base

if TYPE_CHECKING:
    from tg_bot_float_db_app.database.models.relation_model import RelationModel
    from tg_bot_float_db_app.database.models.agent_model import AgentModel
    from tg_bot_float_db_app.database.models.glove_model import GloveModel
else:
    RelationModel = "RelationModel"
    AgentModel = "AgentModel"
    GloveModel = "GloveModel"


class SkinModel(Base):
    __tablename__ = "skin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    relations: Mapped[List[RelationModel]] = relationship(
        back_populates="skin", cascade="all, delete", passive_deletes=True
    )

    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id", ondelete="cascade"), nullable=True)

    agent: Mapped[AgentModel] = relationship(AgentModel, back_populates="skins")

    glove_id: Mapped[int] = mapped_column(ForeignKey("glove.id", ondelete="cascade"), nullable=True)

    glove: Mapped[GloveModel] = relationship(GloveModel, back_populates="skins")
