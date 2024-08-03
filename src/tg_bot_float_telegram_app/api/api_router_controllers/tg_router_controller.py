from fastapi import APIRouter, Request


from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_settings import TgSettings


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

    async def _webhook(self, request: Request) -> None:
        await self._tg_bot_float_app.update_feed(await request.json())
