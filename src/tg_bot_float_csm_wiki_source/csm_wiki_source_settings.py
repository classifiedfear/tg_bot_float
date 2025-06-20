from pydantic_settings import BaseSettings, SettingsConfigDict


class CsmWikiSourceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="tg_bot_float_csm_wiki_source/csm_wiki_source_variables.env",
        env_file_encoding="utf-8",
    )

    base_url: str
    graphql_url: str
    graphql_query: str
    headers: str
