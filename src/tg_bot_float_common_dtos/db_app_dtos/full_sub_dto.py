from tg_bot_float_common_dtos.base_dto import BaseDTO


class FullSubDTO(BaseDTO):
    weapon_id: int
    weapon_name: str
    skin_id: int
    skin_name: str
    quality_id: int
    quality_name: str
    stattrak: bool
