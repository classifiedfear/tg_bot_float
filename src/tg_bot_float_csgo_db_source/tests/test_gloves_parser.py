import pytest

from tg_bot_float_common_dtos.csgo_db_source_dtos.glove_dto import GloveSkinsDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.gloves_parser import GlovesParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@pytest.fixture(scope="module")
def gloves_parser(parser_settings_fixture: ParserSettings) -> GlovesParser:
    return GlovesParser(parser_settings_fixture)


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (GloveSkinsDTO(glove_name="Moto Gloves", skins=["Finish Line", "Polygon"], count=10), 2),
        (
            GloveSkinsDTO(
                glove_name="Sport Gloves", skins=["Nocts", "Omega", "Slingshot"], count=12
            ),
            3,
        ),
        (GloveSkinsDTO(glove_name="Hydra Gloves", skins=["Case Hardened"], count=4), 1),
    ],
)
def test_gloves_parser(
    gloves_parser: GlovesParser,
    gloves_page: str,
    result: GloveSkinsDTO,
    intersection: int,
) -> None:
    page_dto = gloves_parser.get_parsed_data(gloves_page)

    assert len(page_dto.gloves) == 8

    assert sum(map(lambda x: x.count, page_dto.gloves)) == 68

    assert result.count in [dto.count for dto in page_dto.gloves]

    for glove_skins_dto in page_dto.gloves:
        if glove_skins_dto.glove_name == result.glove_name:
            assert len(set(result.skins).intersection(set(glove_skins_dto.skins))) == intersection
            assert result.count == glove_skins_dto.count


def test_gloves_parser_empty_page(gloves_parser: GlovesParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        gloves_parser.get_parsed_data("")

    assert "No gloves found!" in str(exc_info)


def test_gloves_parser_wrong_page(gloves_parser: GlovesParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        gloves_parser.get_parsed_data("test")

    assert "Wrong page request!" in str(exc_info)
