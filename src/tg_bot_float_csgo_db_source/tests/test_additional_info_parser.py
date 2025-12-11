import pytest

from tg_bot_float_common_dtos.csgo_db_source_dtos.additional_info_page_dto import (
    AdditionalInfoPageDTO,
)
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.additional_info_parser import AdditionalInfoParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@pytest.fixture(scope="module")
def additional_info_parser(parser_settings_fixture: ParserSettings) -> AdditionalInfoParser:
    return AdditionalInfoParser(parser_settings_fixture)


@pytest.mark.parametrize(
    ["weapon", "skin", "result"],
    [
        (
            "Five-SeveN",
            "Monkey Business",
            AdditionalInfoPageDTO(
                weapon_name="Five-SeveN",
                skin_name="Monkey Business",
                qualities=["Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"],
                stattrak_qualities=["Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"],
                stattrak_existence=True,
                rarity="Classified",
            ),
        ),
        (
            "P90",
            "Emerald Dragon",
            AdditionalInfoPageDTO(
                weapon_name="P90",
                skin_name="Emerald Dragon",
                qualities=["Minimal Wear", "Field-Tested", "Well-Worn"],
                stattrak_qualities=["Factory New", "Minimal Wear", "Field-Tested"],
                stattrak_existence=True,
                rarity="Classified",
            ),
        ),
        (
            "Skeleton Knife",
            "Slaughter",
            AdditionalInfoPageDTO(
                weapon_name="Skeleton Knife",
                skin_name="Slaughter",
                qualities=["Factory New", "Minimal Wear", "Field-Tested"],
                stattrak_qualities=["Factory New", "Minimal Wear"],
                stattrak_existence=True,
                rarity="Extraordinary",
            ),
        ),
    ],
    indirect=["weapon", "skin"],
)
def test_additional_info_parser(
    additional_info_parser: AdditionalInfoParser,
    additional_info_skin_page: str,
    result: AdditionalInfoPageDTO,
) -> None:
    dto: AdditionalInfoPageDTO = additional_info_parser.get_parsed_data(additional_info_skin_page)
    assert dto == result


def test_additional_info_parser_empty_page(additional_info_parser: AdditionalInfoParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        additional_info_parser.get_parsed_data("")

    assert "No additional info found!" in str(exc_info)


def test_additional_info_parser_wrong_page(additional_info_parser: AdditionalInfoParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        additional_info_parser.get_parsed_data("test")

    assert "Weapon not found in HTML" in str(exc_info)
