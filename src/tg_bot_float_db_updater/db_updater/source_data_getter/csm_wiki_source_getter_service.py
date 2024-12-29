from tg_bot_float_common_dtos.csm_wiki_source_dtos.csm_wiki_dto import CsmWikiDTO
from tg_bot_float_db_updater.db_updater.source_data_getter.abstract_source_data_getter import (
    AbstractSourceGetter,
)


class CsmWikiSourceGetter(AbstractSourceGetter):
    async def get_csm_wiki_skin_data(self, weapon: str, skin: str) -> CsmWikiDTO:
        response = await self._get_response(
            self._settings.csm_wiki_url.format(weapon=weapon, skin=skin)
        )
        if response.get("message"):
            return CsmWikiDTO()
        return CsmWikiDTO.model_validate(response)
