import dataclasses


@dataclasses.dataclass
class SkinDTO:
    name: str = None
    stattrak_existence: bool = False
    id: int = 0
