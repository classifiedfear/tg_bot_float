import pytest


from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import CategoryWeaponsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.weapons_parser import WeaponsParser


from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@pytest.fixture(scope="module")
def weapons_parser(parser_settings_fixture: ParserSettings) -> WeaponsParser:
    return WeaponsParser(parser_settings_fixture)


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (CategoryWeaponsDTO(category="rifles", weapons=["AK-47", "M4A4", "SSG 08"], count=11), 3),
        (CategoryWeaponsDTO(category="smgs", weapons=["UMP-45", "P90"], count=7), 2),
        (CategoryWeaponsDTO(category="knives", weapons=["Talon Knife"], count=20), 1),
    ],
)
def test_weapons_parser(
    weapons_parser: WeaponsParser, weapon_page: str, result: CategoryWeaponsDTO, intersection: int
) -> None:
    page_dto = weapons_parser.get_parsed_data(weapon_page)

    assert len(page_dto.categories) == 6

    assert sum(map(lambda x: x.count, page_dto.categories)) == 55

    for category_weapons_dto in page_dto.categories:
        if category_weapons_dto.category == result.category:
            assert (
                len(set(result.weapons).intersection(set(category_weapons_dto.weapons)))
                == intersection
            )

            assert category_weapons_dto.count == result.count


def test_weapons_parser_empty_page(weapons_parser: WeaponsParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        weapons_parser.get_parsed_data("")

    assert "No weapons found!" in str(exc_info)


def test_weapons_parser_wrong_page(weapons_parser: WeaponsParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        weapons_parser.get_parsed_data("awddwa")

    assert "Wrong page request!" in str(exc_info)
