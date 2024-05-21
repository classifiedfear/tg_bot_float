from pydantic_settings import BaseSettings


class CsmSourceSettings(BaseSettings):
    base_url: str = "https://cs.money/5.0/load_bots_inventory/730"
    params: str = (
        "?hasTradeLock=false&isStatTrak={stattrak}&limit=60"
        "&name={weapon}%20{skin}&offset={offset}&quality={quality}"
    )
