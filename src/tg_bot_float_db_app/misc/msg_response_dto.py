from pydantic import BaseModel


class MsgResponseDTO(BaseModel):
    status: bool
    msg: str
