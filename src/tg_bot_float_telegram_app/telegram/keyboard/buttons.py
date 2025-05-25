from enum import Enum

from tg_bot_float_telegram_app.telegram.constants.general_consts import (
    BUY_TEXT,
    CANCEL_TEXT,
    CONFIRM_TEXT,
    DEFAULT_VERSION_TEXT,
    MY_SUBS_TEXT,
    STATTRAK_VERSION_TEXT,
    SUB_TEXT,
    UNSUB_TEXT,
)


class Buttons(Enum):
    SUB = SUB_TEXT
    UNSUB = UNSUB_TEXT
    MY_SUB = MY_SUBS_TEXT
    BUY = BUY_TEXT
    CONFIRM = CONFIRM_TEXT
    CANCEL = CANCEL_TEXT
    BASE_VERSION = DEFAULT_VERSION_TEXT
    STATTRAK_VERSION = STATTRAK_VERSION_TEXT
