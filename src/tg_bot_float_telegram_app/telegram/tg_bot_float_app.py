from typing import Any, Dict, List

from aiogram import Dispatcher, Bot
from aiogram.types import Update
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis


# from tg_bot_float_common_dtos.tg_result_dtos.tg_result_dto import TgResultDTO
# from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import Keyboard
# from tg_bot_float_telegram_app.tg_constants import RESULT_TEXT
from tg_bot_float_common_dtos.tg_result_dtos.tg_result_dto import TgResultDTO
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import KeyboardController
from tg_bot_float_telegram_app.telegram.constants.tg_constants import RESULT_TEXT
from tg_bot_float_telegram_app.tg_settings import TgSettings
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)


class TgBotFloatApp:
    def __init__(self, settings: TgSettings, redis: Redis) -> None:
        self._settings = settings
        self._bot = Bot(
            token=settings.tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self._dp = Dispatcher(storage=RedisStorage(redis))
        self._controllers: List[AbstractTGRouterController] = []

    def add_tg_router_controller(self, router_controller: AbstractTGRouterController) -> None:
        self._controllers.append(router_controller)

    async def start_bot(self) -> None:
        self._init_router_controllers()
        await self._bot.set_webhook(
            url=self._settings.ngrok_tunnel_url + self._settings.webhook_url,
            allowed_updates=self._dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )

    async def stop_bot(self) -> None:
        await self._bot.delete_webhook()

    def _init_router_controllers(self) -> None:
        self._dp.include_routers(*[controller.router for controller in self._controllers])

    async def update_feed(self, data: Dict[str, Any]) -> None:
        update = Update.model_validate(data, context={"bot": self._bot})
        await self._dp.feed_update(self._bot, update)

    async def send_skin_info(
        self,
        telegram_ids: List[int],
        tg_result_dto: TgResultDTO,
        keyboard: KeyboardController,
    ) -> None:
        for tg_id in telegram_ids:
            for item in tg_result_dto.items_with_benefit:
                await self._bot.send_message(
                    chat_id=tg_id,
                    text=RESULT_TEXT.format(
                        weapon_name=tg_result_dto.subscription_info.weapon_name,
                        skin_name=tg_result_dto.subscription_info.skin_name,
                        quality_name=tg_result_dto.subscription_info.quality_name,
                        stattrak=tg_result_dto.subscription_info.stattrak,
                        name=item.name,
                        benefit_percent=item.benefit_percent,
                        csm_price=item.csm_item_price,
                        csm_overpay_float=item.csm_item_overpay_float,
                        csm_price_with_float=item.csm_item_price_with_float,
                        csm_float=item.csm_item_float,
                        steam_price=item.steam_item_price,
                        steam_float=item.steam_item_float,
                    ),
                    reply_markup=keyboard.create_buy_link(item.steam_buy_link),
                )

    @property
    def bot(self) -> Bot:
        return self._bot
