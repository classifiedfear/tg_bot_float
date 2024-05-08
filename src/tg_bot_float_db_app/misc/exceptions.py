from dataclasses import dataclass


@dataclass
class BotDbException(Exception):
    item: str
    identifier: str
    msg: str
