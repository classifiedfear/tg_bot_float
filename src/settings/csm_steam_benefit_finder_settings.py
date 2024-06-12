from pydantic_settings import BaseSettings


class CsmSteamBenefitFinderSettings(BaseSettings):
    weapon_skin_quality_names_url: str
    user_subscription_url: str
    csm_base_url: str
    steam_base_url: str
    item_url: str
