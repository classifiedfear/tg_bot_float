from pydantic_settings import BaseSettings, SettingsConfigDict


class DbUpdaterSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="tg_bot_float_db_updater/.env", env_file_encoding="utf-8")

    db_update_url: str
    csgo_db_url: str
    csgo_db_weapons_url: str
    csgo_db_skins_url: str
    csm_wiki_url: str
