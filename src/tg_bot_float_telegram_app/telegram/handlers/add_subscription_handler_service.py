from typing import List

from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO

from tg_bot_float_telegram_app.telegram.handlers.handler_service import HandlerService
from tg_bot_float_telegram_app.telegram.states.add_subscription_states import AddSubscriptionStates
from tg_bot_float_telegram_app.telegram.state_controllers.add_subscription_state_controller import (
    AddSubscriptionStateController,
)
from tg_bot_float_telegram_app.telegram.msg_creators.add_subscription_msg_creator import (
    AddSubscriptionMsgCreator,
)

from tg_bot_float_telegram_app.dtos.sub_to_add_dto import SubToAddDTO
from tg_bot_float_telegram_app.user_input_cleaner import UserInputCleaner


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
        user_id: int,
    ) -> None:
        await state_controller.create_user_in_state(user_id)
        await self._prep_weapon_state(msg_creator, state_controller, user_id)

    async def _prep_weapon_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
    ):
        weapons = await self._db_app_service_client.get_weapons()
        await state_controller.update_all_weapons_for_user(user_id, weapons)
        await msg_creator.show_choose_weapon_msg(weapons)
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_WEAPON)

    async def add_subscription_weapon_id(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        index: int,
        user_id: int,
    ):
        weapons_data_dto = await state_controller.get_weapons_data(user_id)
        if UserInputCleaner.check_on_index(weapons_data_dto.len_items, index):
            weapon_index = index - 1
            weapon_dto = weapons_data_dto.items[weapon_index]
            await state_controller.update_weapon_dto_for_user(user_id, weapon_dto)
            skins = await self._db_app_service_client.get_skins_for_weapon_id(weapon_dto.id)
            await self._prep_skin_state(msg_creator, state_controller, user_id, skins)
        else:
            await msg_creator.show_wrong_item_id_msg("оружия")
            return

    async def add_subscription_weapon_user_text(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_text: str,
        user_id: int,
    ):
        weapons_data_dto = await state_controller.get_weapons_data(user_id)
        user_text_cleaned = UserInputCleaner.clean(user_text)
        index = weapons_data_dto.name_to_index.get(user_text_cleaned)
        if index:
            weapon_index = index - 1
            weapon_dto = weapons_data_dto.items[weapon_index]
            await state_controller.update_weapon_dto_for_user(user_id, weapon_dto)
            skins = await self._db_app_service_client.get_skins_for_weapon_id(weapon_dto.id)
            await self._prep_skin_state(msg_creator, state_controller, user_id, skins)
        else:
            await msg_creator.show_wrong_item_name_msg("оружия")
            return

    async def _prep_skin_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
        skins: List[SkinDTO],
    ):
        if not skins:
            await msg_creator.show_weapon_skin_not_exist_msg()
            return
        await msg_creator.show_choose_skin_msg(skins)
        await state_controller.update_all_skins_for_user(user_id, skins)
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_SKIN)

    async def add_subscription_skin_id(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        index: int,
        user_id: int,
    ):
        skins_data_dto = await state_controller.get_skins_data(user_id)
        if UserInputCleaner.check_on_index(skins_data_dto.len_items, index):
            skin_index = index - 1
            skin_dto = skins_data_dto.items[skin_index]
            await state_controller.update_skin_dto_for_user(user_id, skin_dto)
            weapon_dto = await state_controller.get_weapon_dto_for_user(user_id)
            qualities = await self._db_app_service_client.get_qualities_for_weapon_skin_ids(
                weapon_dto.id, skin_dto.id
            )
            await self._prep_quality_state(msg_creator, state_controller, user_id, qualities)
        else:
            await msg_creator.show_wrong_item_id_msg("скина")
            return

    async def add_subscription_skin_user_text(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_text: str,
        user_id: int,
    ):
        skins_data_dto = await state_controller.get_skins_data(user_id)
        user_text_cleaned = UserInputCleaner.clean(user_text)
        index = skins_data_dto.name_to_index.get(user_text_cleaned)
        if index:
            skin_index = index - 1
            skin_dto = skins_data_dto.items[skin_index]
            await state_controller.update_skin_dto_for_user(user_id, skin_dto)
            weapon_dto = await state_controller.get_weapon_dto_for_user(user_id)
            qualities = await self._db_app_service_client.get_qualities_for_weapon_skin_ids(
                weapon_dto.id, skin_dto.id
            )
            await self._prep_quality_state(msg_creator, state_controller, user_id, qualities)
        else:
            await msg_creator.show_wrong_item_name_msg("скина")
            return

    async def _prep_quality_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
        qualities: List[QualityDTO],
    ):
        if not qualities:
            await msg_creator.show_weapon_skin_quality_not_exist_msg()
            return
        await msg_creator.show_choose_quality_msg(qualities)
        await state_controller.update_all_qualities_for_user(user_id, qualities)
        await state_controller.set_state(AddSubscriptionStates.CHOOSE_QUALITY)

    async def add_subscription_quality_id(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        index: int,
        user_id: int,
    ):
        qualities_data_dto = await state_controller.get_qualities_data(user_id)
        if UserInputCleaner.check_on_index(qualities_data_dto.len_items, index):
            quality_index = index - 1
            quality_dto = qualities_data_dto.items[quality_index]
            await state_controller.update_quality_dto_for_user(user_id, quality_dto)
            weapon_dto = await state_controller.get_weapon_dto_for_user(user_id)
            skin_dto = await state_controller.get_skin_dto_for_user(user_id)
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

    async def add_subscription_quality_user_text(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_text: str,
        user_id: int,
    ):
        qualities_data_dto = await state_controller.get_qualities_data(user_id)
        user_text_cleaned = UserInputCleaner.clean(user_text)
        index = qualities_data_dto.name_to_index.get(user_text_cleaned)
        if index:
            quality_index = index - 1
            quality_dto = qualities_data_dto.items[quality_index]
            await state_controller.update_quality_dto_for_user(user_id, quality_dto)
            weapon_dto = await state_controller.get_weapon_dto_for_user(user_id)
            skin_dto = await state_controller.get_skin_dto_for_user(user_id)
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
        user_id: int,
        stattrak: bool | None = None,
    ):
        if stattrak is None:
            await msg_creator.show_choose_variants()
            return
        await state_controller.update_stattrak_for_user(user_id, stattrak)
        await self._prep_finish_subscription_state(msg_creator, state_controller, user_id)

    async def _prep_finish_subscription_state(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
    ):
        weapon_dto = await state_controller.get_weapon_dto_for_user(user_id)
        skin_dto = await state_controller.get_skin_dto_for_user(user_id)
        quality_dto = await state_controller.get_quality_dto_for_user(user_id)
        stattrak_existence = await state_controller.get_stattrak_for_user(user_id)
        await msg_creator.show_confirm_msg(weapon_dto, skin_dto, quality_dto, stattrak_existence)
        await state_controller.set_state(AddSubscriptionStates.CONFIRM_USER_REQUEST)

    async def finish_subscription(
        self,
        msg_creator: AddSubscriptionMsgCreator,
        state_controller: AddSubscriptionStateController,
        user_id: int,
    ):
        user_data_values = await state_controller.get_sub_to_add_dto_for_user(user_id)
        if await self._db_app_service_client.is_subscription_exists(
            user_data_values.tg_user_id,
            user_data_values.weapon_id,
            user_data_values.skin_id,
            user_data_values.quality_id,
            user_data_values.stattrak,
        ):
            await msg_creator.show_already_subscribed_msg()
            await state_controller.clear_states()
            return
        await self._send_create_subscription_request(user_data_values)
        await msg_creator.show_subscribed_msg(user_data_values)
        await state_controller.clear_states()

    async def _send_create_subscription_request(
        self,
        user_data_values: SubToAddDTO,
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
