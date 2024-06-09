from pydantic_settings import BaseSettings


class CsmSteamBenefitFinderSettings(BaseSettings):
    user_subscription_url: str
    csm_base_url: str
    steam_base_url: str
    item_url: str
