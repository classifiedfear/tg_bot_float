from dataclasses import dataclass

from tg_bot_float_common_dtos.source_dtos.steam_item_response_dto import SteamItemResponseDTO
from tg_bot_float_common_dtos.source_dtos.csm_item_response_dto import CsmItemResponseDTO


@dataclass
class SteamCsmMatchDTO:
    steam_item: SteamItemResponseDTO
    csm_item: CsmItemResponseDTO
    percent: float
