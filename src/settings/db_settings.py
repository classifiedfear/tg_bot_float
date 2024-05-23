from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    url: str = f"postgresql+asyncpg://classified:rv9up0ax@192.168.0.200:5432/tg_bot_float_db"
