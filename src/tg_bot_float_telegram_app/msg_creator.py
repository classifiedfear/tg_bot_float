from enum import IntEnum
from typing import List

from aiogram import html

from tg_bot_float_common_dtos.schema_dtos.quality_dto import QualityDTO
from tg_bot_float_common_dtos.schema_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.schema_dtos.weapon_dto import WeaponDTO
from tg_bot_float_telegram_app.db_app_service_client import FullSubscriptionDTO

class WeaponIndex(IntEnum):
    PISTOLS = 1
    AUTO = 11
    SMG = 22
    HEAVY = 29
    KNIFE = 35
    ANOTHER = 55

class AddSubscriptionMsgCreator:
    @staticmethod
    def create_choose_weapon_msg(weapons: List[WeaponDTO]) -> str:
        answer_string = "Введите название оружия из списка: \n"
        for weapon in weapons:
            if weapon.id == WeaponIndex.PISTOLS:
                answer_string += f"\n{html.bold("Пистолеты")}: "
            elif weapon.id == WeaponIndex.AUTO:
                answer_string += f"\n\n{html.bold("Винтовки")}: "
            elif weapon.id == WeaponIndex.SMG:
                answer_string += f"\n\n{html.bold("СМГ")}: "
            elif weapon.id == WeaponIndex.HEAVY:
                answer_string += f"\n\n{html.bold("Тяжелое")}: "
            elif weapon.id == WeaponIndex.KNIFE:
                answer_string += f"\n\n{html.bold("Ножи")}: "
            elif weapon.id == WeaponIndex.ANOTHER:
                answer_string += f"\n\n{html.bold("Другое")}: "
            answer_string += f"\t\t\t({weapon.name})\t\t\t"
        return answer_string

    @staticmethod
    def create_choose_skin(skins: List[SkinDTO]) -> str:
        answer_string = "Введите название скина из списка: \n\n"
        for skin in skins:
            answer_string += f"\t\t\t({skin.name})\t\t\t"
        return answer_string

    @staticmethod
    def create_choose_quality(qualities: List[QualityDTO]) -> str:
        answer_string = "Введите название качества из списка: \n\n"
        for quality in qualities:
            answer_string += f"\t\t\t({quality.name})\t\t\t"
        return answer_string

    @staticmethod
    def create_subscribed_msg(full_subscription_dto: FullSubscriptionDTO) -> str:
        answer_string = "Подписка: "
        full_name = f"{f"{full_subscription_dto.weapon_name}, {full_subscription_dto.skin_name}, {full_subscription_dto.quality_name}, {full_subscription_dto.stattrak}"!r}"
        answer_string += full_name + " была добавлена!"
        return answer_string

    @staticmethod
    def create_watch_subscription_msg(subscriptions: List[FullSubscriptionDTO]) -> str:
        answer_string = "Введите подписку из списка:\n"
        for subscription in subscriptions:
            answer_string += f"\t\t\t({subscription.weapon_name}, {subscription.skin_name}, {subscription.quality_name}, {subscription.stattrak})\t\t\t\n"
        return answer_string


