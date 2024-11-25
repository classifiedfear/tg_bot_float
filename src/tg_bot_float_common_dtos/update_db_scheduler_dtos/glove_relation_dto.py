from pydantic import BaseModel, ConfigDict

from tg_bot_float_common_dtos.schema_dtos.glove_dto import GloveDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO



class GloveRelationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    glove: GloveDTO
    skin: SkinDTO
