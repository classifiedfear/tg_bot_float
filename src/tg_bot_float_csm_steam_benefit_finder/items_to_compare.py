from dataclasses import dataclass, field
from typing import List

from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO


@dataclass
class ItemsToCompareDTO:
    csm_items: List[CsmItemResponseDTO] = field(default_factory=list)
    steam_items: List[SteamItemResponseDTO] = field(default_factory=list)
