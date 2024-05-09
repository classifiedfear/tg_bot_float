class BotDbException(Exception):
    def __init__(self, msg: str, status: int):
        self.msg = msg
        self.status = status

