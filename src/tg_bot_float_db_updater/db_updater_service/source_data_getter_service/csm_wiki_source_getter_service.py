from tg_bot_float_common_dtos.source_dtos.csm_wiki_dto import CsmWikiDTO
from tg_bot_float_db_updater.db_updater_service.source_data_getter_service.abstract_source_getter_service import (
    AbstractSourceGetterService,
)


class CsmWikiSourceGetterService(AbstractSourceGetterService):
    async def get_csm_wiki_skin_data(self, weapon: str, skin: str) -> CsmWikiDTO:
        response = await self._get_response(
            self._settings.csm_wiki_url.format(weapon=weapon, skin=skin)
        )
        return CsmWikiDTO.model_validate(response)
