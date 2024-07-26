from pydantic import BaseModel, ConfigDict


class GraphqlItemDataDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = ""
    isStatTrack: bool = False
