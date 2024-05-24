from __future__ import annotations
from typing import List, Dict, Tuple

from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.relation_dto import RelationDTO
from tg_bot_float_common_dtos.update_db_scheduler_dtos.source_data_tree_dto import SourceDataTreeDTO


class DataTreeFromSource:
    def __init__(self):
        self._all_weapons: Dict[str, WeaponDTO] = {}
        self._all_skins: Dict[str, SkinDTO] = {}
        self._all_qualities: Dict[str, QualityDTO] = {}
        self._all_relations: Dict[Tuple[int, int, int], RelationDTO] = {}

    def add_weapons(self, weapon_names: List[str]) -> List[WeaponDTO]:
        weapons: List[WeaponDTO] = []
        for name in weapon_names:
            weapon_dto = self._all_weapons.setdefault(name, WeaponDTO(name=name))
            weapons.append(weapon_dto)
        return weapons

    def add_skins(self, skin_names: List[str]) -> List[SkinDTO]:
        skins: List[SkinDTO] = []
        for name in skin_names:
            skin_dto = self._all_skins.setdefault(name, SkinDTO(name=name))
            skins.append(skin_dto)
        return skins

    def add_qualities(self, quality_names: List[str]) -> List[QualityDTO]:
        qualities: List[QualityDTO] = []
        for name in quality_names:
            quality_dto = self._all_qualities.setdefault(name, QualityDTO(name=name))
            qualities.append(quality_dto)
        return qualities

    def add_relation(self, weapon: WeaponDTO, skin: SkinDTO, quality: QualityDTO) -> None:
        self._all_relations.setdefault(
            (weapon.name, skin.name, quality.name),
            RelationDTO(weapon=weapon, skin=skin, quality=quality),
        )

    def to_dto(self) -> SourceDataTreeDTO:
        return SourceDataTreeDTO(
            weapons=list(self._all_weapons.values()),
            skins=list(self._all_skins.values()),
            qualities=list(self._all_qualities.values()),
            relations=list(self._all_relations.values()),
        )