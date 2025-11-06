from pydantic_settings import BaseSettings, SettingsConfigDict


class RequestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csgo_db_source/settings/request_variables.env",
        env_file_encoding="utf-8",
    )

    # All variables connected with url_path
    base_domen: str

    weapons_path_url: str
    skins_path_url: str
    additional_info_path_url: str
    gloves_path_url: str
    agents_path_url: str
