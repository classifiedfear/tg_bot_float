from typing import List

from pydantic import BaseModel

from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.agent_relation_dto import AgentRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.glove_relation_dto import GloveRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_data_dto import RelationDataDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO


class SourceDataTreeDTO(BaseModel):
    weapons: List[WeaponDTO]
    skins: List[SkinDTO]
    qualities: List[QualityDTO]
    gloves: List[GloveDTO]
    agents: List[AgentDTO]
    relations: List[RelationDataDTO]
    glove_relations: List[GloveRelationDTO]
    agent_relations: List[AgentRelationDTO]
