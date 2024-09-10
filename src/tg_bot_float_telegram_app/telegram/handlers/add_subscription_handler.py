from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_float_common_dtos.schema_dtos.subscription_dto import SubscriptionDTO
from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.states.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)
from tg_bot_float_telegram_app.tg_constants import (
    ALREADY_SUBSCRIBED_MSG_TEXT,
    BACK_TO_MAIN_MENU_MSG_TEXT,
    CHOOSING_STATTRAK_MSG_TEXT,
    WRONG_ITEM_NAME_MSG_TEXT,
)


class AddSubscriptionHandler:
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient):
        self._keyboard = keyboard
        self._db_app_service_client = db_app_service_client
        self._state_controller = AddSubscriptionStateController()
        self._msg_creator = AddSubscriptionMsgCreator()

    async def cancel(self, message: Message, state: FSMContext):
        await self._state_controller.clear_states(state)
        await message.answer(BACK_TO_MAIN_MENU_MSG_TEXT, reply_markup=self._keyboard.main_buttons)

    async def start_add_subscription(self, message: Message, state: FSMContext) -> None:
        await self._state_controller.set_choosing_weapon_state(state)

        weapons = await self._db_app_service_client.get_weapons()
        await self._state_controller.update_all_weapons(state, weapons)

        answer_string = self._msg_creator.create_choose_weapon_msg(weapons)
        await message.answer(answer_string, reply_markup=self._keyboard.back_button)

    async def add_subscription_weapon(self, message: Message, state: FSMContext):
        if weapon_dto := await self._state_controller.try_get_weapon_from_text(
            state, str(message.text)
        ):
            await self._state_controller.update_weapon_id_name(state, weapon_dto)
            await self._state_controller.set_choosing_skin_state(state)

            skins = await self._db_app_service_client.get_skins_for_weapon_id(weapon_dto.id)

            if not skins:
                await message.answer(
                    "Для этого оружия не существует скинов",
                    reply_markup=self._keyboard.main_buttons,
                )
                return

            await self._state_controller.update_all_skins(state, skins)

            answer_string = self._msg_creator.create_choose_skin(skins)
            await message.answer(answer_string)
        else:
            await message.answer(WRONG_ITEM_NAME_MSG_TEXT.format(item="оружия"))
            return

    async def add_subscription_skin(self, message: Message, state: FSMContext):
        if skin_dto := await self._state_controller.try_get_skin_from_text(
            state, str(message.text)
        ):
            await self._state_controller.update_skin_id_name(state, skin_dto)
            await self._state_controller.set_choosing_quality_state(state)

            weapon_dto = await self._state_controller.get_weapon_dto(state)

            qualities = await self._db_app_service_client.get_qualities_for_weapon_skin_ids(
                weapon_dto.id, skin_dto.id
            )
            await self._state_controller.update_all_qualities(state, qualities)

            answer_string = self._msg_creator.create_choose_quality(qualities)
            await message.answer(answer_string)
        else:
            await message.answer(WRONG_ITEM_NAME_MSG_TEXT.format(item="скина"))
            return

    async def add_subscription_quality(self, message: Message, state: FSMContext):
        if quality_dto := await self._state_controller.try_get_quality_from_text(
            state, str(message.text)
        ):
            await self._state_controller.update_quality_id_name(state, quality_dto)
            await self._state_controller.set_choosing_stattrak_state(state)

            skin_dto = await self._state_controller.get_skin_dto(state)

            stattrak_existence = (
                await self._db_app_service_client.get_stattrak_existence_for_skin_id(skin_dto.id)
            )

            if not stattrak_existence:
                await self._end_subscription(state, message, stattrak_existence)
            else:
                await message.answer(
                    CHOOSING_STATTRAK_MSG_TEXT, reply_markup=self._keyboard.choose_stattrak_buttons
                )
        else:
            await message.answer(WRONG_ITEM_NAME_MSG_TEXT.format(item="качества"))
            return

    async def end_add_subscription(self, message: Message, state: FSMContext):
        stattrak = False
        if str(message.text).lower().strip() == "Stattrak версия".lower():
            stattrak = True
        subscription_dto = await self._state_controller.get_subscription_dto(state, stattrak)
        if await self._db_app_service_client.is_subscription_exists(
            message.from_user.id, subscription_dto
        ):
            await self._state_controller.clear_states(state)
            await message.answer(
                ALREADY_SUBSCRIBED_MSG_TEXT, reply_markup=self._keyboard.main_buttons
            )
            return
        await self._end_subscription(state, message, subscription_dto)

    async def _end_subscription(
        self, state: FSMContext, message: Message, subscription_dto: SubscriptionDTO
    ) -> None:
        await self._send_create_subscription_request(subscription_dto, message.from_user.id)
        await self._state_controller.clear_states(state)
        answer_string = self._msg_creator.create_subscribed_msg(subscription_dto)
        await message.answer(answer_string, reply_markup=self._keyboard.main_buttons)

    async def _send_create_subscription_request(
        self,
        full_subscription_dto: SubscriptionDTO,
        telegram_user_id: int,
    ) -> None:
        user = await self._db_app_service_client.get_user_by_telegram_id(telegram_user_id)
        await self._db_app_service_client.create_subscription(
            user.id,
            full_subscription_dto.weapon_id,
            full_subscription_dto.skin_id,
            full_subscription_dto.quality_id,
            full_subscription_dto.stattrak,
        )
