from pydantic_settings import BaseSettings, SettingsConfigDict


class DbUpdaterSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_db_updater/db_updater_variables.env", env_file_encoding="utf-8"
    )

    db_update_url: str
    csgo_db_url: str
    csgo_db_weapons_url: str
    csgo_db_skins_url: str
    csgo_db_gloves_url: str
    csgo_db_agents_url: str
    csm_wiki_url: str
