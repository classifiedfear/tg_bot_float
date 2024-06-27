class BaseSteamSourceException(Exception):
    """Base class for Steam Source Exceptions"""

    def __init__(self, msg: str):
        self.msg = msg


class IncorrectDataException(BaseSteamSourceException):
    """Exception when user input incorrect data for request"""


class TooManyRequestsException(BaseSteamSourceException):
    """Exception when was done too much requests."""
