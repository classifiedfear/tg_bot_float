from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csgo_db_source/settings/parser_variables.env",
        env_file_encoding="utf-8",
    )
    # All variables connected with WeaponsScrapper
    total_weapon_regex: str
    weapon_name_regex: str
    weapon_category_number_regex: str

    # All variables connected with SkinsScrapper
    skin_weapon_name_regex: str
    skin_name_regex: str
    skin_rarity_regex: str

    # All variables connected with AdditionalInfoScrapper
    quality_stattrak_regex: str
    additional_weapon_skin_name_regex: str
    rarity_regex: str
    collection_regex: str

    # All variables connected with gloves
    glove_regex: str

    # All variables connected with agents
    agent_regex: str
