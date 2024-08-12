from dataclasses import dataclass, field
from typing import List

from tg_bot_float_common_dtos.source_dtos.csm_item_dto import CsmItemDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_dto import SteamItemDTO


@dataclass
class ItemsToCompareDTO:
    csm_items: List[CsmItemDTO] = field(default_factory=list)
    steam_items: List[SteamItemDTO] = field(default_factory=list)
