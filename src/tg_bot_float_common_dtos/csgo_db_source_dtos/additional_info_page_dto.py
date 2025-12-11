from typing import List, Optional

from tg_bot_float_common_dtos.base_dto import BaseDTO


class AdditionalInfoPageDTO(BaseDTO):
    weapon_name: str
    skin_name: str
    rarity: str
    qualities: List[str] = []
    stattrak_qualities: List[str] = []
    stattrak_existence: Optional[bool] = False
