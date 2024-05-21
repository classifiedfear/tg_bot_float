from pydantic_settings import BaseSettings


class CsgoDbSourceSettings(BaseSettings):
    base_url: str = "https://www.csgodatabase.com"
    weapons_page: str = "/weapons"
    skins_page: str = "/weapons/{weapon}"
    retry_when_unauthorized: int = 3
