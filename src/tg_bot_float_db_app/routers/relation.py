import fastapi
import pydantic

from tg_bot_float_db_app.database.models import skin_models
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.contexts.relation import RelationsContext

relation_router = fastapi.APIRouter(
    prefix="/relations",
    tags=["relations"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_wsq_context)]
)


class Relation(pydantic.BaseModel):
    weapon_id: int
    skin_id: int
    quality_id: int


@relation_router.post('')
async def create(relation: Relation, relation_table: RelationsContext = fastapi.Depends(db_dependencies.get_db_wsq_context)):
    relation_dict = relation.model_dump()
    relation_model = skin_models.RelationModel(**relation_dict)
    await relation_table.create(relation_model)
    await relation_table.save_changes()
    return relation_model


@relation_router.get('{weapon_id}/{skin_id}/{quality_id}')
async def get_relation_by_id(
        weapon_id: int, skin_id: int, quality_id: int,
        relation_table: RelationsContext = fastapi.Depends(db_dependencies.get_db_wsq_context)
):
    if result := await relation_table.get_by_id(weapon_id, skin_id, quality_id):
        return result
    else:
        return {"message": "Not found"}


@relation_router.delete('{weapon_id}/{skin_id}/{quality_id}')
async def delete_relation_by_id(
        weapon_id: int, skin_id: int, quality_id: int,
        relation_table: RelationsContext = fastapi.Depends(db_dependencies.get_db_wsq_context)
):
    await relation_table.delete_by_id(weapon_id, skin_id, quality_id)
    await relation_table.save_changes()
    return {'success': True}

@relation_router.put('{weapon_id}/{skin_id}/{quality_id}')
async def update_relation(
        weapon_id: int, skin_id: int, quality_id: int, relation: Relation,
        relation_table: RelationsContext = fastapi.Depends(db_dependencies.get_db_wsq_context)
):
    relation_model = await relation_table.update_by_id(weapon_id, skin_id, quality_id, **relation.model_dump())
    await relation_table.save_changes()
    return relation_model

@relation_router.get('')
async def get_relations(relation_table: RelationsContext = fastapi.Depends(db_dependencies.get_db_wsq_context)):
    return list(await relation_table.get_all())
