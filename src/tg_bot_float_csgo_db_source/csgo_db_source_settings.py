from pydantic_settings import BaseSettings, SettingsConfigDict


class CsgoDbSourceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csgo_db_source/.env", env_file_encoding="utf-8"
    )

    base_url: str
    weapons_page: str
    skins_page: str
    weapon_regex_pattern: str
    skin_regex_pattern: str
    retry_when_unauthorized: int
    not_retry_statuses: str
