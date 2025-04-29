from tg_bot_float_telegram_app.telegram.handlers.handler_service import HandlerService
from tg_bot_float_telegram_app.telegram.msg_creators.command_msg_creator import CommandMsgCreator


class CommandHandlerService(HandlerService):
    async def command_start(self, msg_creator: CommandMsgCreator) -> None:
        await msg_creator.greetings_msg()

    async def show_subscriptions(self, msg_creator: CommandMsgCreator, user_id: int) -> None:
        subscriptions = await self._db_app_service_client.get_subscriptions_by_telegram_id(user_id)
        if not subscriptions:
            await msg_creator.show_no_subscriptions_msg()
            return
        await msg_creator.show_subscriptions_msg(subscriptions)
