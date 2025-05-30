import datetime
from tg_bot_float_common_dtos.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int = 0
    telegram_id: int = 0
    username: str | None = None
    full_name: str | None = None
    reg_date: datetime.datetime | None = None
