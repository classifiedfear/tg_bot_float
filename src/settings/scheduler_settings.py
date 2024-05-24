from pydantic_settings import BaseSettings


class SchedulerSettings(BaseSettings):
    db_update_url: str = "http://192.168.0.200:5001/db/update_db"
    csgo_db_url: str = "http://192.168.0.200:5002"
    csgo_db_weapons_url: str = "/weapons"
    csgo_db_skins_url: str = "/skins/{weapon}"
    csm_wiki_url: str = "http://192.168.0.200:5003/{weapon}/{skin}"
    csm_base_url: str = "http://192.168.0.200:5004/csm"
    steam_base_url: str = "http://192.168.0.200:5005/steam"
    item_url: str = "/{weapon}/{skin}/{quality}/{stattrak}"
