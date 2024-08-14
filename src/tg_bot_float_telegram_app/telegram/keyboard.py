from typing import Any, List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class Keyboard:
    def __init__(self) -> None:
        self._init_buttons()

    def _init_buttons(self) -> None:
        self._main_buttons = self._create_main_buttons()
        self._back_button = self._create_cancel_button()
        self._choose_stattrak_buttons = self._create_choose_stattrak_buttons()

    def _create_main_buttons(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard(["Отслеживать", "Отписаться", "Поиск"])

    def _create_buy_url_button(self, url: str):
        return self._create_inline_keyboard(["Купить"], url=url)

    def _create_cancel_button(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard(["Отменить"])

    def _create_choose_stattrak_buttons(self) -> ReplyKeyboardMarkup:
        return self._create_reply_keyboard(["Базовая версия", "Stattrak версия"])

    @property
    def main_buttons(self) -> ReplyKeyboardMarkup:
        return self._main_buttons

    @property
    def back_button(self) -> ReplyKeyboardMarkup:
        return self._back_button

    @property
    def choose_stattrak_buttons(self) -> ReplyKeyboardMarkup:
        return self._choose_stattrak_buttons

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
