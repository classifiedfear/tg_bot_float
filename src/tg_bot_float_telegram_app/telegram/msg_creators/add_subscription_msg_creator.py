from typing import List


from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_telegram_app.db_app_service_client import SubscriptionDTO
from tg_bot_float_telegram_app.tg_constants import CHOOSING_ITEM_MSG_TEXT, SUBSCRIBED_MSG_TEXT


class AddSubscriptionMsgCreator:
    def __init__(self) -> None:
        self._stattrak_status_msg = "Default"

    def create_choose_weapon_msg(self, weapons: List[WeaponDTO]) -> str:
        return self._create_choosing_msg(
            CHOOSING_ITEM_MSG_TEXT.format(item="оружия"), [str(item.name) for item in weapons]
        )

    def create_choose_skin(self, skins: List[SkinDTO]) -> str:
        return self._create_choosing_msg(
            CHOOSING_ITEM_MSG_TEXT.format(item="скина"), [str(item.name) for item in skins]
        )

    def create_choose_quality(self, qualities: List[QualityDTO]) -> str:
        return self._create_choosing_msg(
            CHOOSING_ITEM_MSG_TEXT.format(item="качества "), [str(item.name) for item in qualities]
        )

    def _create_choosing_msg(self, base_answer: str, items: List[str]) -> str:
        answer_string = base_answer
        for item in items:
            answer_string += f'\t\t\t"{item}",\t\t\t'
        return answer_string

    def create_subscribed_msg(self, subscription_dto: SubscriptionDTO) -> str:
        stattrak_status_msg = self._stattrak_status_msg
        if subscription_dto.stattrak:
            stattrak_status_msg = "Stattrak"
        return SUBSCRIBED_MSG_TEXT.format(
            weapon_name=subscription_dto.weapon_name,
            skin_name=subscription_dto.skin_name,
            quality_name=subscription_dto.quality_name,
            stattrak=stattrak_status_msg,
        )
