from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_db_app/db_app_variables.env", env_file_encoding="utf-8"
    )

    url: str
