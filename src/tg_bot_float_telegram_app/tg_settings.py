from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class TgSettings(BaseSettings):
    # tg specific variables
    tg_token: str

    # db specific variables
    db_url: str
    redis_host_url: str

    # db_app_service_client variables
    db_app_base_url: str
    create_user_url: str
    get_user_url: str
    get_weapons_url: str
    get_skins_for_weapon_id_url: str
    get_qualities_for_weapon_skin_ids_url: str
    get_stattrak_existence_for_skin_id_url: str
    create_subscription_url: str
    get_subscriptions_by_telegram_id_url: str
    get_weapon_skin_quality_names_url: str
    delete_subscription_url: str
    get_users_telegram_ids_by_subscription_url: str
    get_subscription_url: str

    # webhook variables
    ngrok_tunnel_url: str
    webhook_url: str

    model_config = SettingsConfigDict(
        env_file="tg_bot_float_telegram_app/telegram_app_variables.env", env_file_encoding="utf-8"
    )


@lru_cache()
def get_tg_settings() -> TgSettings:
    return TgSettings() #type: ignore "Load from telegram_app_variables.env file."
