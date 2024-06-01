from tg_bot_float_csgo_db_source.services.abstract_page_service import AbstractPageService


class SkinPageService(AbstractPageService):

    async def get_skin_names(self, weapon: str):
        if weapon[0] == "★":
            skin_names = await self._get_item_names(
                self._settings.base_url + self._settings.skins_page.format(weapon=weapon[2:])
            )
        else:
            skin_names = await self._get_item_names(
                self._settings.base_url + self._settings.skins_page.format(weapon=weapon)
            )
        return skin_names[1:]
