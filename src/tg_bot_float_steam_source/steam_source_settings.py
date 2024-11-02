from pydantic_settings import BaseSettings, SettingsConfigDict


class SteamSourceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_steam_source/steam_source_variables.env", env_file_encoding="utf-8"
    )

    base_url: str
    item_url: str
    not_retry_statuses: str
    params: str
    item_buy_url: str
    float_info_url: str
    steam_market_source_headers: str
    steam_float_source_headers: str
    render: str
