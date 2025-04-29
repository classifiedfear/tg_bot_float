import pickle
from typing import List

from fastapi import APIRouter, Request
import brotli


from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import KeyboardController
from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_settings import TgSettings
from tg_bot_float_common_dtos.tg_result_dtos.tg_result_dto import TgResultDTO


class TgRouterController:
    _router = APIRouter()

    def __init__(
        self,
        settings: TgSettings,
        keyboard: KeyboardController,
        tg_bot_float_app: TgBotFloatApp,
        db_app_service_client: DBAppServiceClient,
    ):
        self._settings = settings
        self._db_app_service_client = db_app_service_client
        self._keyboard = keyboard
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
        tg_result_dto: TgResultDTO = pickle.loads(to_unpickle)
        if tg_result_dto.items_with_benefit:
            telegram_ids: List[int] = (
                await self._db_app_service_client.get_users_telegram_ids_by_subscription(
                    tg_result_dto.subscription_info
                )
            )
            await self._tg_bot_float_app.send_skin_info(telegram_ids, tg_result_dto, self._keyboard)
