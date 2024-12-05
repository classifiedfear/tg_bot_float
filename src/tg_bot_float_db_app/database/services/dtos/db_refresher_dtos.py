from typing import Dict, Generic, List, TypeVar

from pydantic import BaseModel

from tg_bot_float_common_dtos.schema_dtos.relation_id_dto import RelationIdDTO

ModelT = TypeVar("ModelT")


class CreateDeleteDTO(BaseModel, Generic[ModelT]):
    dtos_to_create: Dict[str, ModelT]
    names_to_delete: List[str]


class IdRelationsCreateDeleteDTO(BaseModel):
    ids_relations_to_create: List[RelationIdDTO]
    ids_relations_to_delete: List[RelationIdDTO]
