from tg_bot_float_common_dtos.schema_dtos.base_dto import BaseDTO


class SubscriptionToFindDTO(BaseDTO):
    weapon_id: int
    skin_id: int
    quality_id: int
    stattrak: bool
    count: int
