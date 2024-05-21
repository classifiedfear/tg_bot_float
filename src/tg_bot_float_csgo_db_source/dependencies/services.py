from typing import Annotated

from fastapi import Depends

from tg_bot_float_csgo_db_source.services.weapon_page_service import WeaponPageService
from tg_bot_float_csgo_db_source.services.skin_page_service import SkinPageService

WEAPON_PAGE_SERVICE = Annotated[WeaponPageService, Depends(WeaponPageService)]

SKIN_PAGE_SERVICE = Annotated[SkinPageService, Depends(SkinPageService)]
