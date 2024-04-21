import typing

import fastapi
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.tables.skin_table import SkinTable
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.models.skin_models import SkinModel

skin_router = fastapi.APIRouter(
    prefix="/skins",
    tags=["skins"])


class SkinPostModel(BaseModel):
    name: str
    stattrak_existence: bool = False


@skin_router.post("/create")
async def create(
        skin_post_model: SkinPostModel,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = SkinModel(**skin_post_model.model_dump())
    try:
        await skin_context.create(skin_db_model)
    except IntegrityError:
        return {"success": False, "message": f"Skin with this name already exists, names need to be unique!"}
    await skin_context.save_changes()
    return skin_db_model


@skin_router.get("/id/{id}")
async def get_skin_by_id(
        id: int,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if skin_db_model := await skin_context.get_by_id(id):
        return skin_db_model
    else:
        return {"status": False, "message": f"Skin with id - {str(id)!r} does not exist!"}


@skin_router.put("/id/{id}")
async def update_skin_by_id(
        id: int,
        skin_post_model: SkinPostModel,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = await skin_context.get_by_id(id)
    if skin_db_model is None:
        return {"status": False, "message": f"Skin with id - {str(id)!r} does not exist!"}
    try:
        skin_db_model.name = skin_post_model.name
        skin_db_model.stattrak_existence = skin_post_model.stattrak_existence
        await skin_context.save_changes()
        return skin_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Weapon with name {skin_post_model.name!r} already exists, names need be unique!"}


@skin_router.delete("/id/{id}")
async def delete_skin_by_id(
        id: int,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if await skin_context.delete_by_id(id):
        await skin_context.save_changes()
        return {'success': True, "message": f"Skin with id - {str(id)!r} deleted"}
    return {"success": False, "message": f'Skin with id - {str(id)!r} does not exist!'}


@skin_router.get('/name/{name}')
async def get_skin_by_name(
        name: str,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if skin_db_model := await skin_context.get_by_name(name):
        return skin_db_model
    else:
        return {"status": False, "message": f"Skin with name - {name!r} does not exist!"}


@skin_router.put('/name/{name')
async def update_skin_by_name(
        name: str,
        skin_post_model: SkinPostModel,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = await skin_context.get_by_name(name)
    if skin_db_model is None:
        return {"status": False, "message": f"Skin with name - {name!r} does not exist!"}
    try:
        skin_db_model.name = skin_post_model.name
        skin_db_model.stattrak_existence = skin_post_model.stattrak_existence
        await skin_context.save_changes()
        return skin_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Skin with name {skin_post_model.name!r} already exists, names need be unique!"}


@skin_router.delete('/name/{name}')
async def delete_skin_by_name(
        name: str,
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if await skin_context.delete_by_name(name):
        await skin_context.save_changes()
        return {'success': True, "message": f"Skin with name - {name!r} deleted"}
    return {"success": False, "message": f'Skin with id - {name!r} does not exist!'}


@skin_router.post('/create_many')
async def create_many(
        skin_post_models: typing.List[SkinPostModel],
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    weapon_db_models = [SkinModel(**skin_post_model.model_dump()) for skin_post_model in skin_post_models]
    try:
        await skin_context.create_many(weapon_db_models)
    except IntegrityError:
        return {"success": False, "message": "Skin names should be unique!"}
    await skin_context.save_changes()
    return weapon_db_models

@skin_router.get('/')
async def get_many(skin_table: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)):
    return list(await skin_table.get_all())


@skin_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    existence_skin_db_models = await skin_context.get_many_by_id(ids)
    ids_on_delete = [skin_db_model.id for skin_db_model in existence_skin_db_models]
    not_found_ids = [id for id in ids if id not in ids_on_delete]
    if ids_on_delete:
        await skin_context.delete_many_by_id(ids_on_delete)
        await skin_context.save_changes()
        return {
            'success': True,
            'message': f'Skin with ids: {ids_on_delete} deleted. {f'{not_found_ids} not found' if not_found_ids else ''}'}
    return {"success": False, "message": f"Skin with {ids} not found"}


@skin_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        skin_context: SkinTable = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    existence_skin_db_models = await skin_context.get_many_by_name(names)
    names_on_delete = [skin_db_model.name for skin_db_model in existence_skin_db_models]
    not_found_names = [name for name in names if name not in names_on_delete]
    if names_on_delete:
        await skin_context.delete_many_by_name(names_on_delete)
        await skin_context.save_changes()
        return {
            'success': True,
            'message': f'Skin with name {names_on_delete} deleted. {f'{not_found_names} not found' if not_found_names else ''}'
        }
    return {"success": False, "message": f"Skin with names {names} not found"}
