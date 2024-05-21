from pydantic_settings import BaseSettings


class SteamSourceSettings(BaseSettings):
    base_url: str = "https://steamcommunity.com/market/listings/730/"
    item_url: str = "{stattrak}{weapon}%20%7C%20{skin}%20%28{quality}%29"
    render: str = "/render/"
    params: str = "?query=&start={start}&count={count}&currency={currency}"
    item_buy_url: str = "?filter=#buylisting|{listing_id}|{app_id}|{context_id}|{asset_id}"
    float_info_url: str = "https://api.csfloat.com/?url={inspect_link}"
