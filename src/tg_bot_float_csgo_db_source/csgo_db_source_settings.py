from pydantic_settings import BaseSettings, SettingsConfigDict


class CsgoDbSourceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csgo_db_source/csgo_db_source_variables.env",
        env_file_encoding="utf-8",
    )

    base_url: str
    weapons_page: str
    gloves_page: str
    gloves_skin_page: str
    agents_page: str
    skins_page: str
    weapon_regex_pattern: str
    skin_regex_pattern: str
    glove_regex_pattern: str
    agent_regex_pattern: str
    first_knife_weapon: str
    first_other_weapon: str
