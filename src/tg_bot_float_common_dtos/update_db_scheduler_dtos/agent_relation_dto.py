from pydantic import BaseModel, ConfigDict

from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO


class AgentRelationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    agent: AgentDTO
    skin: SkinDTO
