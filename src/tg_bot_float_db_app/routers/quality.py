import typing

import fastapi
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.tables.quality_table import QualityTable
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.models.skin_models import QualityModel

quality_router = fastapi.APIRouter(
    prefix="/qualities",
    tags=["qualities"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_quality_context)]
)


class QualityPostModel(BaseModel):
    name: str


@quality_router.post('/create')
async def create(
        quality_post_model: QualityPostModel,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    quality_db_model = QualityModel(**quality_post_model.model_dump())
    try:
        await quality_context.create(quality_db_model)
    except IntegrityError:
        return {"success": False, "message": f"Quality with this name already exists, names need to be unique!"}
    await quality_context.save_changes()
    return quality_db_model


@quality_router.get('/id/{id}')
async def get_weapon_by_id(
        id: int,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    if quality_db_model := await quality_context.get_by_id(id):
        return quality_db_model
    else:
        return {"status": False, "message": f"Quality with id - {str(id)!r} does not exist!"}


@quality_router.put('/id/{id}')
async def update_weapon_by_id(
        id: int,
        quality_post_model: QualityPostModel,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    quality_db_model = await quality_context.get_by_id(id)
    if quality_db_model is None:
        return {"status": False, "message": f"Quality with id - {str(id)!r} does not exist!"}
    try:
        quality_db_model.name = quality_post_model.name
        await quality_context.save_changes()
        return quality_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Quality with name {quality_post_model.name!r} already exists, names need be unique!"}


@quality_router.delete('/id/{id}')
async def delete_weapon_by_id(
        id: int,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    if await quality_context.delete_by_id(id):
        await quality_context.save_changes()
        return {'success': True, "message": f"Quality with id - {str(id)!r} deleted"}
    return {"success": False, "message": f'Quality with id - {str(id)!r} does not exist!'}


@quality_router.get('/name/{name}')
async def get_weapon_by_name(
        name: str,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    if quality_db_model := await quality_context.get_by_name(name):
        return quality_db_model
    else:
        return {"status": False, "message": f"Quality with name - {name!r} does not exist!"}


@quality_router.put('/name/{name}')
async def update_weapon_by_name(
        name: str,
        quality_post_model: QualityPostModel,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    weapon_db_model = await quality_context.get_by_name(name)
    if weapon_db_model is None:
        return {"status": False, "message": f"Quality with name - {name!r} does not exist!"}
    try:
        weapon_db_model.name = quality_post_model.name
        await quality_context.save_changes()
        return weapon_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Quality with name {quality_post_model.name!r} already exists, names need be unique!"}


@quality_router.delete('/name/{name}')
async def delete_weapon_by_name(
        name: str,
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    if await quality_context.delete_by_name(name):
        await quality_context.save_changes()
        return {'success': True, "message": f"Quality with name - {name!r} deleted"}
    return {"success": False, "message": f'Quality with id - {name!r} does not exist!'}


@quality_router.post('/create_many')
async def create_many(
        quality_post_models: typing.List[QualityPostModel],
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    quality_db_models = [QualityModel(**quality_post_model.model_dump()) for quality_post_model in quality_post_models]
    try:
        await quality_context.create_many(quality_db_models)
    except IntegrityError:
        return {"success": False, "message": "Quality names should be unique!"}
    await quality_context.save_changes()
    return quality_db_models


@quality_router.get('/')
async def get_many(quality_table: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)):
    return list(await quality_table.get_all())


@quality_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    existence_quality_db_models = await quality_context.get_many_by_id(ids)
    ids_on_delete = [quality_db_model.id for quality_db_model in existence_quality_db_models]
    not_found_ids = [id for id in ids if id not in ids_on_delete]
    if ids_on_delete:
        await quality_context.delete_many_by_id(ids_on_delete)
        await quality_context.save_changes()
        return {
            'success': True,
            'message': f'Quality with ids: {ids_on_delete} deleted. {f'{not_found_ids} not found' if not_found_ids else ''}'}
    return {"success": False, "message": f"Quality with {ids} not found"}


@quality_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        quality_context: QualityTable = fastapi.Depends(db_dependencies.get_db_quality_context)
):
    existence_quality_db_models = await quality_context.get_many_by_name(names)
    names_on_delete = [quality_db_model.name for quality_db_model in existence_quality_db_models]
    not_found_names = [name for name in names if name not in names_on_delete]
    if names_on_delete:
        await quality_context.delete_many_by_name(names_on_delete)
        await quality_context.save_changes()
        return {
            'success': True,
            'message': f'Quality with name {names_on_delete} deleted. {f'{not_found_names} not found' if not_found_names else ''}'
        }
    return {"success": False, "message": f"Quality with names {names} not found"}

