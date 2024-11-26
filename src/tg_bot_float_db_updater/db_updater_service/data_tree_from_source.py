from __future__ import annotations
from collections import defaultdict
from typing import List, Dict, Tuple

from tg_bot_float_common_dtos.schema_dtos.agent_dto import AgentDTO
from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.agent_relation_dto import AgentRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.glove_relation_dto import GloveRelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO


class DataTreeFromSource:
    def __init__(self) -> None:
        self._all_weapons: Dict[str, WeaponDTO] = {}
        self._all_skins: Dict[str, SkinDTO] = {}
        self._all_qualities: Dict[str, QualityDTO] = {}
        self._all_gloves: Dict[str, GloveDTO] = {}
        self._all_agents: Dict[str, AgentDTO] = {}
        self._all_relations: Dict[Tuple[str, str, str], RelationDTO] = {}
        self._all_glove_relations: Dict[str, List[SkinDTO]] = defaultdict(list)
        self._all_agent_relations: Dict[str, List[SkinDTO]] = defaultdict(list)

    def add_weapons(self, weapon_names: List[str]) -> List[WeaponDTO]:
        return [self._all_weapons.setdefault(name, WeaponDTO(name=name)) for name in weapon_names]

    def add_skins(self, skin_names: List[str]) -> List[SkinDTO]:
        return [self._all_skins.setdefault(name, SkinDTO(name=name)) for name in skin_names]

    def add_qualities(self, quality_names: List[str]) -> List[QualityDTO]:
        return [
            self._all_qualities.setdefault(name, QualityDTO(name=name)) for name in quality_names
        ]

    def add_gloves(self, glove_names: List[str]) -> List[GloveDTO]:
        return [
            self._all_gloves.setdefault(glove_name, GloveDTO(name=glove_name))
            for glove_name in glove_names
        ]

    def add_agents(self, agent_fraction_names: List[str]) -> List[AgentDTO]:
        return [
            self._all_agents.setdefault(fraction_name, AgentDTO(name=fraction_name))
            for fraction_name in agent_fraction_names
        ]

    def add_agent_relations(self, agent: AgentDTO, skin: SkinDTO) -> None:
        self._all_agent_relations[str(agent.name)].append(skin)

    def add_glove_relations(self, glove: GloveDTO, skin: SkinDTO) -> None:
        self._all_glove_relations[str(glove.name)].append(skin)

    def add_relation(self, weapon: WeaponDTO, skin: SkinDTO, quality: QualityDTO) -> None:
        self._all_relations.setdefault(
            (str(weapon.name), str(skin.name), str(quality.name)),
            RelationDTO(weapon=weapon, skin=skin, quality=quality),
        )

    def to_dto(self) -> SourceDataTreeDTO:
        return SourceDataTreeDTO(
            weapons=list(self._all_weapons.values()),
            skins=list(self._all_skins.values()),
            qualities=list(self._all_qualities.values()),
            relations=list(self._all_relations.values()),
            gloves=list(self._all_gloves.values()),
            agents=list(self._all_agents.values()),
            glove_relations=[
                GloveRelationDTO(glove=self._all_gloves[glove_name], skins=skins)
                for glove_name, skins in self._all_glove_relations.items()
            ],
            agent_relations=[
                AgentRelationDTO(agent=self._all_agents[agent_name], skins=skins)
                for agent_name, skins in self._all_agent_relations.items()
            ],
        )
