from pydantic import BaseModel, ConfigDict


class FloatItemInfoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_item_name: str = ""
    floatvalue: float = 0
