from pydantic_settings import BaseSettings


class CsgoDbSourceSettings(BaseSettings):
    base_url: str = "https://www.csgodatabase.com"
    weapons_page: str = "/weapons"
    skins_page: str = "/weapons/{weapon}"
    weapon_regex_pattern: str = r'<h3 class="item-box-header.+">([\w\s-]+)<\/h3>'
    skin_regex_pattern: str = r"<span class='block txt-med txt-white'>([\w\s'-]+)<\/span>"
    retry_when_unauthorized: int = 3
