from typing import Any, List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from tg_bot_float_telegram_app.telegram.keyboard.buttons import Buttons


class Keyboard:
    def __init__(self) -> None:
        self._init_buttons()

    def _init_buttons(self) -> None:
        self._main_buttons = self._create_main_buttons()
        self._back_button = self._create_cancel_button()
        self._choose_stattrak_buttons = self._create_choose_stattrak_buttons()
        self._confirm_buttons = self._create_confirm_buttons()

    def _create_main_buttons(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard(
            [Buttons.SUB.value, Buttons.UNSUB.value, Buttons.MY_SUB.value]
        )

    def _create_buy_url_button(self, url: str):
        return self._create_inline_keyboard([Buttons.BUY.value], url=url)

    def _create_cancel_button(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard([Buttons.CANCEL.value])

    def _create_choose_stattrak_buttons(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard(
            [Buttons.BASE_VERSION.value, Buttons.STATTRAK_VERSION.value]
        )

    def _create_confirm_buttons(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard([Buttons.CONFIRM.value, Buttons.CANCEL.value])

    @property
    def main_buttons(self) -> ReplyKeyboardMarkup:
        return self._main_buttons

    @property
    def back_button(self) -> ReplyKeyboardMarkup:
        return self._back_button

    @property
    def choose_stattrak_buttons(self) -> ReplyKeyboardMarkup:
        return self._choose_stattrak_buttons

    @property
    def confirm_buttons(self) -> ReplyKeyboardMarkup:
        return self._confirm_buttons

    def create_buy_link(self, link: str) -> InlineKeyboardMarkup:
        return self._create_inline_keyboard(["Купить в стиме"], url=link)

    def _create_reply_keyboard(
        self, buttons_text: List[str], *row_sizes: int
    ) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for text in buttons_text:
            builder.button(text=text)
            builder.adjust(*row_sizes)
        return builder.as_markup()

    def _create_inline_keyboard(
        self, buttons_text: List[str], *row_sizes: int, **inline_button_kwargs: Any
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for text in buttons_text:
            builder.button(text=text, **inline_button_kwargs)
            builder.adjust(*row_sizes)
        return builder.as_markup()
