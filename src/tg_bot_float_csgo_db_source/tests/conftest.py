from pathlib import Path
import pytest

from tg_bot_float_csgo_db_source.settings.parser_settings import ParserSettings
from tg_bot_float_csgo_db_source.settings.request_settings import RequestSettings


@pytest.fixture(scope="session")
def weapon_page() -> str:
    with open(
        Path("tg_bot_float_csgo_db_source/tests/html_pages/weapons_page.txt"),
        "r",
        encoding="UTF-8",
    ) as file:
        return file.read()


@pytest.fixture(scope="session")
def weapon(request: pytest.FixtureRequest) -> str:
    return request.param.lower().replace(" ", "_").replace("-", "_")


@pytest.fixture(scope="session")
def skin(request: pytest.FixtureRequest) -> str:
    return request.param.lower().replace(" ", "_").replace("-", "_")


@pytest.fixture(scope="session")
def skin_page(weapon: str) -> str:
    with open(
        Path(f"tg_bot_float_csgo_db_source/tests/html_pages/{weapon}_skin_page.txt"),
        "r",
        encoding="UTF-8",
    ) as file:
        return file.read()


@pytest.fixture(scope="session")
def additional_info_skin_page(weapon: str, skin: str) -> str:
    with open(
        Path(
            f"tg_bot_float_csgo_db_source/tests/html_pages/{weapon}_{skin}_additional_info_page.txt"
        ),
        "r",
        encoding="UTF-8",
    ) as file:
        return file.read()


@pytest.fixture(scope="session")
def gloves_page() -> str:
    with open(
        Path("tg_bot_float_csgo_db_source/tests/html_pages/gloves_page.txt"), "r", encoding="UTF-8"
    ) as file:
        return file.read()


@pytest.fixture(scope="session")
def agents_page() -> str:
    with open(
        Path("tg_bot_float_csgo_db_source/tests/html_pages/agents_page.txt"), "r", encoding="UTF-8"
    ) as file:
        return file.read()


@pytest.fixture(scope="session")
def request_settings_fixture():
    return RequestSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"


@pytest.fixture(scope="session")
def parser_settings_fixture():
    return ParserSettings()  # type: ignore "Load variables from 'csgo_db_source_variables.env file'"
