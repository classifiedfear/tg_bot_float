from collections import defaultdict
import re
from typing import Dict, List


from tg_bot_float_common_dtos.csgo_database_source_dtos.gloves_page_response_dto import (
    GlovesPageResponseDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_source_settings import CsgoDbSourceSettings

from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class GlovesPageService(AbstractPageService):
    def __init__(self, settings: CsgoDbSourceSettings) -> None:
        super().__init__(settings)
        self._glove_regex = re.compile(self._settings.glove_regex_pattern)

    async def get_glove_names(self) -> List[GlovesPageResponseDTO]:
        gloves: Dict[str, List[str]] = defaultdict(list)
        response_text = await self._get_response(
            self._settings.base_url + self._settings.gloves_page
        )
        for match in self._glove_regex.finditer(response_text):
            gloves[match.group(1)].append(match.group(2))
        return [
            GlovesPageResponseDTO(glove_name=glove_name, skins=skins)
            for glove_name, skins in gloves.items()
        ]
