import pytest

from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import WeaponSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.skins_parser import SkinsParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@pytest.fixture(scope="module")
def skins_parser(parser_settings_fixture: ParserSettings) -> SkinsParser:
    return SkinsParser(parser_settings_fixture)


@pytest.mark.parametrize(
    ["weapon", "items_len", "sum_items", "result", "intersection"],
    [
        (
            "Desert Eagle",
            5,
            42,
            WeaponSkinsDTO(
                weapon_name="Desert Eagle",
                skins=["Naga", "Serpent Strike", "Trigger Discipline"],
                rarity="Restricted",
                count=14,
            ),
            3,
        ),
        (
            "Famas",
            6,
            40,
            WeaponSkinsDTO(
                weapon_name="FAMAS",
                skins=["Contrast Spray", "Colony"],
                rarity="Consumer",
                count=5,
            ),
            2,
        ),
        (
            "Karambit",
            1,
            24,
            WeaponSkinsDTO(
                weapon_name="Karambit",
                skins=["Lore", "Marble Fade", "Ultraviolet"],
                rarity="Extraordinary",
                count=24,
            ),
            3,
        ),
    ],
    indirect=["weapon"],
)
def test_skins_parser(
    skins_parser: SkinsParser,
    skin_page: str,
    items_len: int,
    sum_items: int,
    result: WeaponSkinsDTO,
    intersection: int,
) -> None:
    dto: SkinsPageDTO = skins_parser.get_parsed_data(skin_page)

    assert len(dto.skins) == items_len

    assert sum(map(lambda x: x.count, dto.skins)) == sum_items

    assert dto.weapon_name == dto.weapon_name

    for weapon_skin_dto in dto.skins:
        if result.rarity == weapon_skin_dto.rarity:
            assert weapon_skin_dto.count == result.count

            assert len(set(result.skins).intersection(set(weapon_skin_dto.skins))) == intersection


def test_skins_parser_empty_page(
    skins_parser: SkinsParser,
) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        skins_parser.get_parsed_data("")

    assert "No skins found" in str(exc_info)


def test_skins_parser_wrong_page(skins_parser: SkinsParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        skins_parser.get_parsed_data("awddwa")

    assert "Weapon not found in HTML" in str(exc_info)
