from tg_bot_float_common_dtos.schema_dtos.base_dto import BaseDTO


class SkinDTO(BaseDTO):
    id: int = 0
    name: str | None = None
    stattrak_existence: bool = False
