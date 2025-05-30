from tg_bot_float_common_dtos.base_dto import BaseDTO


class SubscriptionDTO(BaseDTO):
    id: int = 0
    user_id: int = 0
    weapon_id: int | None = 0
    skin_id: int | None = 0
    quality_id: int | None = 0
    stattrak: bool | None = None
