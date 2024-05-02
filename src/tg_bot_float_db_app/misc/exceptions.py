class BotDbExceptions(Exception):
    """Base class for bot db exceptions"""

class BotDbDeleteException(BotDbExceptions):
    """Error for basic deletion operations,
    when the number of deleted rows does not match the
    requested rows for deletion"""