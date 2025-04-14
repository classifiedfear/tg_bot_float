#from typing import List
#from tg_bot_float_common_dtos.schema_dtos.subscription_dto import UserDataValues
#from tg_bot_float_telegram_app.tg_constants import DELETED_SUBSCRIPTION_TEXT
#
#
#class DeleteSubscriptionMsgCreator:
#    def __init__(self) -> None:
#        self._stattrak_status_msg = "Default"
#
#    def create_watch_subscription_msg(self, subscriptions: List[UserDataValues]) -> str:
#        answer_string = "Введите подписку из списка:\n"
#        for subscription in subscriptions:
#            stattrak_status_msg = self._stattrak_status_msg
#            if subscription.stattrak:
#                stattrak_status_msg = "Stattrak"
#            answer_string += (
#                "\t\t\t"
#                f'"{subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {stattrak_status_msg}"'
#                "\t\t\t\n"
#            )
#        return answer_string
#
#    def create_delete_subscription_msg(self, subscription_dto: UserDataValues) -> str:
#        stattrak_status_msg = self._stattrak_status_msg
#        if subscription_dto.stattrak:
#            stattrak_status_msg = "Stattrak"
#        return DELETED_SUBSCRIPTION_TEXT.format(
#            weapon_name=subscription_dto.weapon_name,
#            skin_name=subscription_dto.skin_name,
#            quality_name=subscription_dto.quality_name,
#            stattrak=stattrak_status_msg,
#        )
