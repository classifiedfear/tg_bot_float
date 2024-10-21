from __future__ import annotations
from typing import List, Dict, Tuple

from tg_bot_float_common_dtos.csgo_database_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.csgo_database_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO


class DataTreeFromSource:
    def __init__(self) -> None:
        self._all_weapons: Dict[str, WeaponDTO] = {}
        self._all_skins: Dict[str, SkinDTO] = {}
        self._all_qualities: Dict[str, QualityDTO] = {}
        self._all_gloves: Dict[str, GlovesPageDTO] = {}
        self._all_agents: Dict[str, AgentsPageDTO] = {}
        self._all_relations: Dict[Tuple[str, str, str], RelationDTO] = {}

    def add_weapons(self, weapon_names: List[str]) -> List[WeaponDTO]:
        return [self._all_weapons.setdefault(name, WeaponDTO(name=name)) for name in weapon_names]

    def add_skins(self, skin_names: List[str]) -> List[SkinDTO]:
        return [self._all_skins.setdefault(name, SkinDTO(name=name)) for name in skin_names]

    def add_qualities(self, quality_names: List[str]) -> List[QualityDTO]:
        return [
            self._all_qualities.setdefault(name, QualityDTO(name=name)) for name in quality_names
        ]

    def add_gloves(self, gloves_page_dtos: List[GlovesPageDTO]) -> List[GlovesPageDTO]:
        return [
            self._all_gloves.setdefault(gloves_page_dto.glove_name, gloves_page_dto)
            for gloves_page_dto in gloves_page_dtos
        ]

    def add_agents(self, agents_page_dtos: List[AgentsPageDTO]) -> List[AgentsPageDTO]:
        return [
            self._all_agents.setdefault(agents_page_dto.fraction_name, agents_page_dto)
            for agents_page_dto in agents_page_dtos
        ]

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
        )
