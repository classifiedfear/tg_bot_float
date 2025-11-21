from typing import List
from dataclasses import dataclass, field

from tg_bot_float_common_dtos.csm_source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.steam_source_dtos.steam_item_dto import SteamItemDTO


@dataclass
class CsmSteamItemsToCompareDTO:
    csm_items: List[CsmItemDTO] = field(default_factory=list)
    steam_items: List[SteamItemDTO] = field(default_factory=list)
