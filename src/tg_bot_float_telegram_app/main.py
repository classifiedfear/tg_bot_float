from typing import Any, AsyncGenerator, List
from fastapi import FastAPI
from redis.asyncio import Redis

from tg_bot_float_telegram_app.api.api_router_controllers.tg_router_controller import (
    TgRouterController,
)

from tg_bot_float_telegram_app.service_client.db_app_service_client import DbAppServiceClient
from tg_bot_float_telegram_app.telegram.handlers.add_subscription_handler_service import (
    AddSubscriptionHandlerService,
)
from tg_bot_float_telegram_app.telegram.handlers.command_handler_service import (
    CommandHandlerService,
)
from tg_bot_float_telegram_app.telegram.handlers.delete_subscripton_handler import (
    DeleteSubscriptionHandlerService,
)
from tg_bot_float_telegram_app.telegram.keyboard.keyboard_controller import KEYBOARD_CONTROLLER
from tg_bot_float_telegram_app.telegram.midlewares.prep_middleware import PrepMiddleware
from tg_bot_float_telegram_app.telegram.midlewares.register_check import RegisterCheckMiddleware
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.msg_creators.command_msg_creator import CommandMsgCreator

from tg_bot_float_telegram_app.telegram.msg_creators.delete_subscription_msg_creator import (
    DeleteSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.telegram.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.state_controllers.delete_subscription_state_controller import (
    DeleteSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.abstract_router_controller import (
    AbstractTGRouterController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.command_router_controller import (
    CommandRouterController,
)

from tg_bot_float_telegram_app.telegram.telegram_routers.add_subscription_router_controller import (
    AddSubscriptionRouterController,
)
from tg_bot_float_telegram_app.telegram.telegram_routers.delete_subscription_router_controller import (
    DeleteSubscriptionRouterController,
)
from tg_bot_float_telegram_app.telegram.tg_bot_float_app import TgBotFloatApp
from tg_bot_float_telegram_app.tg_settings import get_tg_settings


TG_SETTINGS = get_tg_settings()
REDIS_STORAGE = Redis(host=TG_SETTINGS.redis_host_url)


tg_app = TgBotFloatApp(TG_SETTINGS, REDIS_STORAGE)
db_app_service_client = DbAppServiceClient(TG_SETTINGS)

fastapi_routers = [
    TgRouterController(TG_SETTINGS, KEYBOARD_CONTROLLER, tg_app, db_app_service_client)
]


def get_command_router_controller() -> CommandRouterController:
    msg_creator = CommandMsgCreator(KEYBOARD_CONTROLLER)
    hanlder = CommandHandlerService(
        db_app_service_client,
        REDIS_STORAGE,
    )
    middleware = PrepMiddleware(msg_creator)
    outer_middleware = RegisterCheckMiddleware(db_app_service_client, REDIS_STORAGE)
    return CommandRouterController(hanlder, middleware, outer_middleware)


def get_add_subscription_router_controller() -> AddSubscriptionRouterController:
    msg_creator = AddSubscriptionMsgCreator(KEYBOARD_CONTROLLER)
    state_controller = AddSubscriptionStateController()
    handler = AddSubscriptionHandlerService(
        db_app_service_client,
        REDIS_STORAGE,
    )
    middleware = PrepMiddleware(msg_creator, state_controller)
    return AddSubscriptionRouterController(handler, middleware)


def get_delete_subscription_router_controller() -> DeleteSubscriptionRouterController:
    msg_creator = DeleteSubscriptionMsgCreator(KEYBOARD_CONTROLLER)
    state_controller = DeleteSubscriptionStateController()
    handler = DeleteSubscriptionHandlerService(
        db_app_service_client,
        REDIS_STORAGE,
    )
    middleware = PrepMiddleware(msg_creator, state_controller)
    return DeleteSubscriptionRouterController(handler, middleware)


tg_routers: List[AbstractTGRouterController] = [
    get_command_router_controller(),
    get_add_subscription_router_controller(),
    get_delete_subscription_router_controller(),
]

for tg_router in tg_routers:
    tg_app.add_tg_router_controller(tg_router)


async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, Any]:
    await tg_app.start_bot()
    yield
    await tg_app.stop_bot()
    await REDIS_STORAGE.close()
    await db_app_service_client.close()


app = FastAPI(lifespan=lifespan)


for router in fastapi_routers:
    app.include_router(router.router)
