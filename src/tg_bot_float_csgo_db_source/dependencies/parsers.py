from typing import Annotated

from fastapi import Depends

from tg_bot_float_csgo_db_source.dependencies.settings import PARSER_SETTINGS
from tg_bot_float_csgo_db_source.parsers.additional_info_parser import AdditionalInfoParser
from tg_bot_float_csgo_db_source.parsers.agents_parser import AgentsParser
from tg_bot_float_csgo_db_source.parsers.gloves_parser import GlovesParser
from tg_bot_float_csgo_db_source.parsers.skins_parser import SkinsParser
from tg_bot_float_csgo_db_source.parsers.weapons_parser import WeaponsParser


def get_weapons_parser(parser_settings: PARSER_SETTINGS) -> WeaponsParser:
    return WeaponsParser(parser_settings)


def get_skins_parser(parser_settings: PARSER_SETTINGS) -> SkinsParser:
    return SkinsParser(parser_settings)


def get_additional_info_parser(parser_settings: PARSER_SETTINGS) -> AdditionalInfoParser:
    return AdditionalInfoParser(parser_settings)


def get_gloves_parser(parser_settings: PARSER_SETTINGS) -> GlovesParser:
    return GlovesParser(parser_settings)


def get_agents_parser(parser_settings: PARSER_SETTINGS) -> AgentsParser:
    return AgentsParser(parser_settings)


WEAPONS_PARSER = Annotated[WeaponsParser, Depends(get_weapons_parser)]

SKINS_PARSER = Annotated[SkinsParser, Depends(get_skins_parser)]

ADDITIONAL_INFO_PARSER = Annotated[AdditionalInfoParser, Depends(get_additional_info_parser)]

GLOVES_PARSER = Annotated[GlovesParser, Depends(get_gloves_parser)]

AGENTS_PARSER = Annotated[AgentsParser, Depends(get_agents_parser)]
