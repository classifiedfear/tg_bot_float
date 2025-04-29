from aiogram.types import Message

from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import KeyboardController


class MsgCreator:
    _message: Message

    def __init__(self, keyboard_controller: KeyboardController) -> None:
        self._keyboard_controller = keyboard_controller

    def change_messager(self, message: Message) -> None:
        self._message = message
