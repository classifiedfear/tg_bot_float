from pydantic_settings import BaseSettings, SettingsConfigDict


class CsmSourceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csm_source/.env", env_file_encoding="utf-8"
    )
    base_url: str
    params: str
    headers: str
