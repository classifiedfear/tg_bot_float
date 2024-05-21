from pydantic_settings import BaseSettings


class CsmWikiSourceSettings(BaseSettings):
    base_url: str = "https://wiki.cs.money"
    graphql_url: str = "/api/graphql"
