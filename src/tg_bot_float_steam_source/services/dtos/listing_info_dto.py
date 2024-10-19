from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class ListingInfoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    asset: Dict[str, Any]
    listingid: str
    converted_price_per_unit: int
    converted_fee_per_unit: int
