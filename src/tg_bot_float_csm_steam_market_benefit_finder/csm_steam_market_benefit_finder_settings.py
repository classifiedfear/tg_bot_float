from pydantic_settings import BaseSettings, SettingsConfigDict


class CsmSteamMarketBenefitFinderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csm_steam_market_benefit_finder/csm_steam_market_benefit_finder_variables.env",
        env_file_encoding="utf-8",
    )

    db_app_base_url: str
    get_item_names_for_subscription_url: str
    get_user_subscription_url: str
    csm_base_url: str
    steam_base_url: str
    get_item_url: str
    telegram_app_base_url: str
    send_update_url: str
