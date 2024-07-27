class CsmSourceExceptions(Exception):
    """Class for error where invalid input."""

    def __init__(self, msg: str):
        self.msg = msg
