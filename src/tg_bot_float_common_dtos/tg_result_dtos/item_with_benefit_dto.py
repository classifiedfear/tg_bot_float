from dataclasses import dataclass


@dataclass
class ItemWithBenefitDTO:
    name: str
    steam_item_float: float
    steam_item_price: float
    steam_buy_link: str
    csm_item_float: float
    csm_item_price: float
    csm_item_price_with_float: float
    csm_item_overpay_float: float
    benefit_percent: float
