from tg_bot_float_common_dtos.schema_dtos.base_dto import BaseDTO


class RelationIdDTO(BaseDTO):
    weapon_id: int = 0
    skin_id: int = 0
    quality_id: int = 0
    stattrak_existence: bool | None = None
