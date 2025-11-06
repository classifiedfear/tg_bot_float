from typing import Annotated

from fastapi import Depends

from tg_bot_float_common_dtos.csgo_db_source_dtos.additional_info_page_dto import (
    AdditionalInfoPageDTO,
)

from tg_bot_float_common_dtos.csgo_db_source_dtos.page_dto import PageDTO


from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import SkinDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import WeaponDTO
from tg_bot_float_csgo_db_source.dependencies.parsers import (
    ADDITIONAL_INFO_PARSER,
    AGENTS_PARSER,
    GLOVES_PARSER,
    SKINS_PARSER,
    WEAPONS_PARSER,
)
from tg_bot_float_csgo_db_source.dependencies.response_service import (
    CSGO_DB_SOURCE_RESPONSE_SERVICE,
)

from tg_bot_float_csgo_db_source.services.csgo_db_source_service import CsgoDbSourceService


async def get_weapon_page_service(
    response_service: CSGO_DB_SOURCE_RESPONSE_SERVICE, parser: WEAPONS_PARSER
) -> CsgoDbSourceService[PageDTO[WeaponDTO]]:
    return CsgoDbSourceService(response_service, parser)


async def get_skins_page_service(
    response_service: CSGO_DB_SOURCE_RESPONSE_SERVICE, parser: SKINS_PARSER
) -> CsgoDbSourceService[PageDTO[SkinDTO]]:
    return CsgoDbSourceService(response_service, parser)


async def get_additional_info_page_service(
    response_service: CSGO_DB_SOURCE_RESPONSE_SERVICE,
    additional_info_parser: ADDITIONAL_INFO_PARSER,
) -> CsgoDbSourceService[AdditionalInfoPageDTO]:
    return CsgoDbSourceService(response_service, additional_info_parser)


async def get_gloves_page_service(
    response_service: CSGO_DB_SOURCE_RESPONSE_SERVICE, parser: GLOVES_PARSER
) -> CsgoDbSourceService[PageDTO[SkinDTO]]:
    return CsgoDbSourceService(response_service, parser)


async def get_agents_page_service(
    response_service: CSGO_DB_SOURCE_RESPONSE_SERVICE, parser: AGENTS_PARSER
) -> CsgoDbSourceService[PageDTO[SkinDTO]]:
    return CsgoDbSourceService(response_service, parser)


WEAPON_PAGE_SERVICE = Annotated[
    CsgoDbSourceService[PageDTO[WeaponDTO]], Depends(get_weapon_page_service)
]

SKINS_PAGE_SERVICE = Annotated[
    CsgoDbSourceService[PageDTO[SkinDTO]], Depends(get_skins_page_service)
]

ADDITIONAL_INFO_PAGE_SERVICE = Annotated[
    CsgoDbSourceService[AdditionalInfoPageDTO], Depends(get_additional_info_page_service)
]

GLOVES_PAGE_SERVICE = Annotated[
    CsgoDbSourceService[PageDTO[SkinDTO]], Depends(get_gloves_page_service)
]

AGENTS_PAGE_SERVICE = Annotated[
    CsgoDbSourceService[PageDTO[SkinDTO]], Depends(get_agents_page_service)
]
