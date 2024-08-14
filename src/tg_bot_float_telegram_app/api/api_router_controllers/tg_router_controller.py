import pickle
from typing import List

from fastapi import APIRouter, Request
import brotli


from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_constants import RESULT_MSG_TEXT
from tg_bot_float_telegram_app.tg_settings import TgSettings
from tg_bot_float_common_dtos.tg_result import TgResult


class TgRouterController:
    _router = APIRouter()

    def __init__(self, settings: TgSettings, tg_bot_float_app: TgBotFloatApp):
        self._settings = settings
        self._tg_bot_float_app = tg_bot_float_app
        self._init_routes()

    @property
    def router(self):
        return self._router

    def _init_routes(self):
        self._router.add_api_route(self._settings.webhook_url, self._webhook, methods=["POST"])
        self._router.add_api_route("/send_update", self._send_subscription_update, methods=["GET"])

    async def _webhook(self, request: Request) -> None:
        await self._tg_bot_float_app.update_feed(await request.json())

    async def _send_subscription_update(self, request: Request) -> None:
        to_unpickle = brotli.decompress(await request.body())
        tg_result_dto: TgResult = pickle.loads(to_unpickle)
        if tg_result_dto.items_with_benefit:
            telegram_ids: List[int] = (
                await self._tg_bot_float_app.db_app_service_client.get_users_telegram_ids_by_subscription(
                    tg_result_dto.subscription_info
                )
            )
            for tg_id in telegram_ids:
                for item in tg_result_dto.items_with_benefit:
                    await self._tg_bot_float_app.bot.send_message(
                        chat_id=tg_id,
                        text=RESULT_MSG_TEXT.format(
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
                        reply_markup=self._tg_bot_float_app.keyboard.create_buy_link(
                            item.steam_buy_link
                        ),
                    )
