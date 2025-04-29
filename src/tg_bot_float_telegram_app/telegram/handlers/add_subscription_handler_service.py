from typing import List

from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO

from tg_bot_float_telegram_app.telegram.handlers.handler_service import HandlerService
from tg_bot_float_telegram_app.telegram.keyboard.buttons import Buttons
from tg_bot_float_telegram_app.telegram.states.add_subscription_states import AddSubscriptionStates
from tg_bot_float_telegram_app.telegram.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)

from tg_bot_float_telegram_app.dtos.add_user_values_dto import AddUserDataValues


class AddSubscriptionHandlerService(HandlerService):
    async def cancel(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ) -> None:
        await state_controller.clear_states()
        await msg_creator.show_cancel_msg()

    async def start_add_subscription(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ) -> None:
        await self._prep_weapon_state(msg_creator, state_controller)

    async def _prep_weapon_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        weapons = await self._db_app_service_client.get_weapons()
        await state_controller.update_all_weapons(weapons)
        await msg_creator.show_choose_weapon_msg(weapons)
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_WEAPON)

    async def add_subscription_weapon(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        msg_from_user: str,
        user_id: int,
    ):
        if weapon_dto := await state_controller.try_get_weapon_from_user_msg(msg_from_user):
            await state_controller.update_weapon_id_name_for_user(user_id, weapon_dto)
            skins = await self._db_app_service_client.get_skins_for_weapon_id(weapon_dto.id)
            await self._prep_skin_state(msg_creator, state_controller, skins)
        else:
            await msg_creator.show_wrong_item_name_msg("оружия")
            return

    async def _prep_skin_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        skins: List[SkinDTO],
    ):
        if await self._show_skins(msg_creator, skins):
            await state_controller.update_all_skins(skins)
            await state_controller.set_state(AddSubscriptionStates.CHOOSE_SKIN)

    async def _show_skins(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        skins: List[SkinDTO],
    ) -> bool:
        if not skins:
            await msg_creator.show_weapon_skin_not_exist_msg()
            return False

        await msg_creator.show_choose_skin_msg(skins)
        return True

    async def add_subscription_skin(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_msg: str,
        user_id: int,
    ):
        if skin_dto := await state_controller.try_get_skin_from_user_msg(user_msg):
            await state_controller.update_skin_id_name_for_user(user_id, skin_dto)
            weapon_dto = await state_controller.get_weapon_dto(user_id)
            qualities = await self._db_app_service_client.get_qualities_for_weapon_skin_ids(
                weapon_dto.id, skin_dto.id
            )
            await self._prep_quality_state(msg_creator, state_controller, qualities)
        else:
            await msg_creator.show_wrong_item_name_msg("скина")
            return

    async def _prep_quality_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        qualities: List[QualityDTO],
    ):
        await state_controller.update_all_qualities(qualities)
        await msg_creator.show_choose_quality_msg(qualities)
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_QUALITY)

    async def add_subscription_quality(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_msg: str,
        user_id: int,
    ):
        if quality_dto := await state_controller.try_get_quality_from_user_msg(user_msg):
            await state_controller.update_quality_id_name_for_user(user_id, quality_dto)
            skin_dto = await state_controller.get_skin_dto(user_id)
            weapon_dto = await state_controller.get_weapon_dto(user_id)
            stattrak_existence = (
                await self._db_app_service_client.get_stattrak_existence_for_skin_id(
                    weapon_dto.id, skin_dto.id, quality_dto.id
                )
            )
            if not stattrak_existence:
                await self._prep_finish_subscription_state(msg_creator, state_controller, user_id)
            else:
                await self._prep_stattrak_state(msg_creator, state_controller)
        else:
            await msg_creator.show_wrong_item_name_msg("качества")
            return

    async def _prep_stattrak_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
    ):
        await msg_creator.show_choose_stattrak_msg()
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_STATTRAK)

    async def add_subscription_stattrak(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_msg: str,
        user_id: int,
    ):
        if Buttons.STATTRAK_VERSION.value.lower() == user_msg.lower().strip():
            await state_controller.update_stattrak_for_user(user_id, True)
            await self._prep_finish_subscription_state(msg_creator, state_controller, user_id)
        elif Buttons.BASE_VERSION.value.lower() == user_msg.lower().strip():
            await state_controller.update_stattrak_for_user(user_id, False)
            await self._prep_finish_subscription_state(msg_creator, state_controller, user_id)
        else:
            await msg_creator.show_choose_variants()
            return

    async def _prep_finish_subscription_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
    ):
        weapon_dto = await state_controller.get_weapon_dto(user_id)
        skin_dto = await state_controller.get_skin_dto(user_id)
        quality_dto = await state_controller.get_quality_dto(user_id)
        stattrak_existence = await state_controller.get_stattrak(user_id)
        await msg_creator.show_confirm_msg(weapon_dto, skin_dto, quality_dto, stattrak_existence)
        await state_controller.set_state(AddSubscriptionStates.CONFIRM_USER_REQUEST)

    async def finish_subscription(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_msg: str,
        user_id: int,
    ):
        if Buttons.CONFIRM.value.lower() == user_msg.lower().strip():
            user_data_values = await state_controller.get_user_data_values(user_id)
            if await self._db_app_service_client.is_subscription_exists(user_data_values):
                await msg_creator.show_already_subscribed_msg()
                await state_controller.clear_states()
                return
            await self._send_create_subscription_request(user_data_values)
            await msg_creator.show_subscribed_msg(user_data_values)
            await state_controller.clear_states()
        if Buttons.CANCEL.value.lower() == user_msg.lower().strip():
            await msg_creator.show_back_to_main_menu_msg()
            await state_controller.clear_states()

    async def _send_create_subscription_request(
        self,
        user_data_values: AddUserDataValues,
    ) -> None:
        if db_user_id := await self._redis.get(str(user_data_values.tg_user_id)):
            await self._db_app_service_client.create_subscription(
                db_user_id.decode("utf-8"),
                user_data_values.weapon_id,
                user_data_values.skin_id,
                user_data_values.quality_id,
                user_data_values.stattrak,
            )
        else:
            user = await self._db_app_service_client.get_user_by_telegram_id(
                user_data_values.tg_user_id
            )
            await self._db_app_service_client.create_subscription(
                user.id,
                user_data_values.weapon_id,
                user_data_values.skin_id,
                user_data_values.quality_id,
                user_data_values.stattrak,
            )
