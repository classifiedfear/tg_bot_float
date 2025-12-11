from typing import AsyncGenerator, Callable
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from httpx import Response
from pytest_mock import MockFixture

from tg_bot_float_common_dtos.csgo_db_source_dtos.additional_info_page_dto import (
    AdditionalInfoPageDTO,
)
from tg_bot_float_common_dtos.csgo_db_source_dtos.agent_dto import AgentSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.agents_page_dto import AgentsPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.glove_dto import GloveSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.gloves_page_dto import GlovesPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skin_dto import WeaponSkinsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.skins_page_dto import SkinsPageDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapon_dto import CategoryWeaponsDTO
from tg_bot_float_common_dtos.csgo_db_source_dtos.weapons_page_dto import WeaponsPageDTO
from tg_bot_float_csgo_db_source.main import app


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        yield ac


@pytest.fixture
def mock_response_service(mocker: MockFixture) -> Callable[[str], None]:
    def _apply(page: str):
        mocker.patch(
            "tg_bot_float_csgo_db_source.response_service.csgo_db_response_service.CsgoDbSourceResponseService.get_page_html",
            new=mocker.AsyncMock(return_value=page),
        )

    return _apply


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (CategoryWeaponsDTO(category="other", weapons=["Zeus x27"], count=1), 1),
        (CategoryWeaponsDTO(category="pistols", weapons=["Glock-18", "Desert Eagle"], count=10), 2),
        (
            CategoryWeaponsDTO(
                category="knives",
                weapons=["Kukri Knife", "Stiletto Knife", "Shadow Daggers"],
                count=20,
            ),
            3,
        ),
    ],
)
@pytest.mark.asyncio
async def test_weapons_endpoint(
    mock_response_service: Callable[[str], None],
    client: AsyncClient,
    weapon_page: str,
    result: CategoryWeaponsDTO,
    intersection: int,
) -> None:
    mock_response_service(weapon_page)
    response: Response = await client.get("/weapons")

    assert response.status_code == 200

    page_dto = WeaponsPageDTO.model_validate(response.json())

    assert len(page_dto.categories) == 6

    assert sum(map(lambda dto: dto.count, page_dto.categories)) == 55

    assert result.category in [dto.category for dto in page_dto.categories]

    assert result.count in [dto.count for dto in page_dto.categories]

    for result_dto in page_dto.categories:
        if result_dto.category == result.category:
            assert len(set(result.weapons).intersection(set(result_dto.weapons))) == intersection


@pytest.mark.parametrize(
    ("weapon", "weapon_skins_dto", "item_len", "item_sum", "intersection"),
    [
        (
            "Desert Eagle",
            WeaponSkinsDTO(
                weapon_name="Desert Eagle", skins=["Golden Koi"], rarity="Covert", count=4
            ),
            5,
            42,
            1,
        ),
        (
            "FAMAS",
            WeaponSkinsDTO(
                weapon_name="FAMAS", skins=["Doomkitty", "Teardown"], rarity="Mil-spec", count=12
            ),
            6,
            40,
            2,
        ),
        (
            "Karambit",
            WeaponSkinsDTO(
                weapon_name="Karambit",
                skins=["Fade", "Stained", "Crimson Web"],
                rarity="Extraordinary",
                count=24,
            ),
            1,
            24,
            3,
        ),
    ],
    indirect=["weapon"],
)
@pytest.mark.asyncio
async def test_skins_endpoint(
    mock_response_service: Callable[[str], None],
    client: AsyncClient,
    weapon_skins_dto: WeaponSkinsDTO,
    skin_page: str,
    item_len: int,
    item_sum: int,
    intersection: int,
) -> None:
    mock_response_service(skin_page)
    response: Response = await client.get(f"/{weapon_skins_dto.weapon_name}/skins")

    assert response.status_code == 200

    page_dto = SkinsPageDTO.model_validate(response.json())

    assert len(page_dto.skins) == item_len

    assert sum(map(lambda dto: dto.count, page_dto.skins)) == item_sum

    assert page_dto.weapon_name == weapon_skins_dto.weapon_name

    for result_dto in page_dto.skins:
        if weapon_skins_dto.rarity == result_dto.rarity:
            assert result_dto.count == weapon_skins_dto.count
            assert (
                len(set(weapon_skins_dto.skins).intersection(set(result_dto.skins))) == intersection
            )


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
@pytest.mark.asyncio
async def test_additional_info_endpoint(
    mock_response_service: Callable[[str], None],
    additional_info_skin_page: str,
    client: AsyncClient,
    result: AdditionalInfoPageDTO,
) -> None:
    mock_response_service(additional_info_skin_page)
    response: Response = await client.get(f"/{result.weapon_name}/{result.skin_name}")
    assert response.status_code == 200
    page_dto = AdditionalInfoPageDTO.model_validate(response.json())
    assert page_dto == result


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (
            GloveSkinsDTO(
                glove_name="Broken Fang Gloves",
                skins=["Jade", "Needle Point", "Unhinged", "Yellow-banded"],
                count=4,
            ),
            4,
        ),
        (
            GloveSkinsDTO(
                glove_name="Bloodhound Gloves",
                skins=["Bronzed", "Charred", "Guerrilla", "Snakebite"],
                count=4,
            ),
            4,
        ),
        (
            GloveSkinsDTO(
                glove_name="Specialist Gloves",
                skins=["Buckshot", "Crimson Kimono", "Crimson Web"],
                count=11,
            ),
            3,
        ),
    ],
)
@pytest.mark.asyncio
async def test_gloves_endpoint(
    mock_response_service: Callable[[str], None],
    client: AsyncClient,
    gloves_page: str,
    result: GloveSkinsDTO,
    intersection: int,
) -> None:
    mock_response_service(gloves_page)
    response: Response = await client.get("/gloves")

    assert response.status_code == 200

    page_dto = GlovesPageDTO.model_validate(response.json())

    assert len(page_dto.gloves) == 8

    assert sum(map(lambda x: x.count, page_dto.gloves)) == 68

    assert result.glove_name in [dto.glove_name for dto in page_dto.gloves]

    assert result.count in [dto.count for dto in page_dto.gloves]

    for result_dto in page_dto.gloves:
        if result_dto.glove_name == result.glove_name:
            assert len(set(result.skins).intersection(set(result_dto.skins))) == intersection


@pytest.mark.parametrize(
    ["result", "intersection"],
    [
        (
            AgentSkinsDTO(
                fraction_name="Gendarmerie Nationale",
                skins=[
                    "Chef d'Escadron Rouchard",
                    "Chem-Haz Capitaine",
                    "Officer Jacques Beltram",
                    "Sous-Lieutenant Medic",
                    "Aspirant",
                ],
                count=5,
            ),
            5,
        ),
        (
            AgentSkinsDTO(
                fraction_name="The Professionals",
                skins=[
                    "Bloody Darryl The Strapped",
                    "Sir Bloody Loudmouth Darryl",
                    "Sir Bloody Miami Darryl",
                    "Sir Bloody Darryl Royale",
                ],
                count=10,
            ),
            4,
        ),
        (
            AgentSkinsDTO(
                fraction_name="Brazilian 1st Battalion",
                skins=["Primeiro Tenente"],
                count=1,
            ),
            1,
        ),
    ],
)
@pytest.mark.asyncio
async def test_agents_endpoint(
    mock_response_service: Callable[[str], None],
    client: AsyncClient,
    agents_page: str,
    result: AgentSkinsDTO,
    intersection: int,
) -> None:
    mock_response_service(agents_page)
    response: Response = await client.get("/agents")

    assert response.status_code == 200

    page_dto = AgentsPageDTO.model_validate(response.json())

    assert len(page_dto.agents) == 20

    assert sum(map(lambda x: x.count, page_dto.agents)) == 55

    assert result.fraction_name in [dto.fraction_name for dto in page_dto.agents]

    assert result.count in [dto.count for dto in page_dto.agents]

    for result_dto in page_dto.agents:
        if result_dto.fraction_name == result.fraction_name:
            assert len(set(result.skins).intersection(set(result_dto.skins))) == intersection
