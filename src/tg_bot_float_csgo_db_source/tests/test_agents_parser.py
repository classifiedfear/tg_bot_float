import pytest

from tg_bot_float_common_dtos.csgo_db_source_dtos.agent_dto import AgentSkinsDTO
from tg_bot_float_csgo_db_source.csgo_db_exception import CsgoDbException
from tg_bot_float_csgo_db_source.parsers.agents_parser import AgentsParser
from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings


@pytest.fixture(scope="module")
def agents_parser(parser_settings_fixture: ParserSettings) -> AgentsParser:
    return AgentsParser(parser_settings_fixture)


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (
            AgentSkinsDTO(
                fraction_name="SWAT",
                skins=["1st Lieutenant Farlow", "Sergeant Bombson", "Chem-Haz Specialist"],
                count=6,
            ),
            3,
        ),
        (
            AgentSkinsDTO(
                fraction_name="Sabre",
                skins=["Dragomir", "Rezan The Ready", "Blackwolf", "Rezan the Redshirt"],
                count=6,
            ),
            4,
        ),
    ],
)
def test_agents_parser(
    agents_parser: AgentsParser,
    agents_page: str,
    result: AgentSkinsDTO,
    intersection: int,
) -> None:
    page_dto = agents_parser.get_parsed_data(agents_page)

    assert len(page_dto.agents) == 20

    assert sum(map(lambda x: x.count, page_dto.agents)) == 55

    for agent_skins_dto in page_dto.agents:
        if agent_skins_dto.fraction_name == result.fraction_name:
            assert result.count == agent_skins_dto.count

            assert len(set(result.skins).intersection(set(agent_skins_dto.skins))) == intersection


def test_agents_parser_empty_page(agents_parser: AgentsParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        agents_parser.get_parsed_data("")

    assert "No agents found!" in str(exc_info)


def test_agents_parser_wrong_page(agents_parser: AgentsParser) -> None:
    with pytest.raises(CsgoDbException) as exc_info:
        agents_parser.get_parsed_data("test")

    assert "Wrong page request!" in str(exc_info)
