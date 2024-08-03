from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_float_common_dtos.schema_dtos.full_subscription_dto import FullSubscriptionDTO
from tg_bot_float_telegram_app.db_app_service_client import DBAppServiceClient
from tg_bot_float_telegram_app.telegram.keyboard import Keyboard
from tg_bot_float_telegram_app.telegram.state_controller import AddSubscriptionStateController
from tg_bot_float_telegram_app.msg_creator import AddSubscriptionMsgCreator


class AddSubscriptionHandler:
    def __init__(self, keyboard: Keyboard, db_app_service_client: DBAppServiceClient):
        self._keyboard = keyboard
        self._db_app_service_client = db_app_service_client
        self._state_controller = AddSubscriptionStateController()

    async def cancel(self, message: Message, state: FSMContext):
        await self._state_controller.clear_states(state)
        await message.answer("Возвращаю в главное меню", reply_markup=self._keyboard.main_buttons)

    async def start_add_subscription(self, message: Message, state: FSMContext) -> None:
        await self._state_controller.set_choosing_weapon_state(state)

        weapons = await self._db_app_service_client.get_weapons()
        await self._state_controller.update_all_weapons(state, weapons)

        answer_string = AddSubscriptionMsgCreator.create_choose_weapon_msg(weapons)
        await message.answer(answer_string, reply_markup=self._keyboard.back_button)

    async def add_subscription_weapon(self, message: Message, state: FSMContext):
        if weapon_dto := await self._state_controller.try_get_weapon_from_text(
            state, str(message.text)
        ):
            await self._state_controller.update_weapon_id_name(state, weapon_dto)
            await self._state_controller.set_choosing_skin_state(state)

            skins = await self._db_app_service_client.get_skins_for_weapon_id(weapon_dto.id)

            await self._state_controller.update_all_skins(state, skins)

            answer_string = AddSubscriptionMsgCreator.create_choose_skin(skins)
            await message.answer(answer_string)
        else:
            await message.answer("Вы должны выбрать правильное название оружия из списка!")
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

            answer_string = AddSubscriptionMsgCreator.create_choose_quality(qualities)
            await message.answer(answer_string)
        else:
            await message.answer("Вы должны выбрать правильное название скина из списка!")
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
                    "Выберете статтрек:", reply_markup=self._keyboard.choose_stattrak_buttons
                )
        else:
            await message.answer("Вы должны выбрать правильное название качества из списка!")
            return

    async def end_add_subscription(self, message: Message, state: FSMContext):
        stattrak = False
        if str(message.text).lower().strip() == "Stattrak версия".lower():
            stattrak = True
        await self._end_subscription(state, message, stattrak)

    async def _end_subscription(self, state: FSMContext, message: Message, stattrak: bool) -> None:
        full_subscription_dto = await self._state_controller.get_full_subscription_dto(
            state, stattrak
        )
        await self._send_create_subscription_request(full_subscription_dto, message.from_user.id)
        await self._state_controller.clear_states(state)
        answer_string = AddSubscriptionMsgCreator.create_subscribed_msg(full_subscription_dto)
        await message.answer(answer_string, reply_markup=self._keyboard.main_buttons)

    async def _send_create_subscription_request(
        self, full_subscription_dto: FullSubscriptionDTO, telegram_user_id: int,
    ) -> None:
        user = await self._db_app_service_client.get_user_by_telegram_id(
            telegram_user_id
        )
        await self._db_app_service_client.create_subscription(
            user.id,
            full_subscription_dto.weapon_id,
            full_subscription_dto.skin_id,
            full_subscription_dto.quality_id,
            full_subscription_dto.stattrak,
        )
