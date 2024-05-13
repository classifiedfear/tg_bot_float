import dataclasses


@dataclasses.dataclass
class ItemRequestDTO:
    weapon: str
    skin: str
    quality: str
    stattrak: bool
