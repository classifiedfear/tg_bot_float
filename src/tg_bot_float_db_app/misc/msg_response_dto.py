import dataclasses

@dataclasses.dataclass
class MsgResponseDTO:
    status: bool
    msg: str