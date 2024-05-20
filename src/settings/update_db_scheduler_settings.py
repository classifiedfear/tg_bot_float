from pydantic_settings import BaseSettings


class SchedulerSettings(BaseSettings):
    db_update_url: str
    csgo_db_url: str
    csgo_db_weapons_url: str
    csgo_db_skins_url: str
    csm_wiki_url: str
    csm_base_url: str
    steam_base_url: str
    item_url: str
