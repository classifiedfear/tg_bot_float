class SteamSourceException(Exception):
    """Base class for Steam Source Exceptions"""

    def __init__(self, msg: str):
        self.msg = msg
