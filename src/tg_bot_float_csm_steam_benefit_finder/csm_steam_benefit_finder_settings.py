from pydantic_settings import BaseSettings, SettingsConfigDict


class CsmSteamBenefitFinderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csm_steam_benefit_finder/csm_steam_benefit_finder_variables.env",
        env_file_encoding="utf-8",
    )

    db_app_base_url: str
    weapon_skin_quality_names_url: str
    user_subscription_url: str
    csm_base_url: str
    steam_base_url: str
    item_url: str