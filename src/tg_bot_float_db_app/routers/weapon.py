import typing

import fastapi
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.contexts.weapon import WeaponContext
from tg_bot_float_db_app.database.models.skin_models import WeaponModel
from tg_bot_float_db_app.dependencies import db_dependencies


class WeaponPostModel(BaseModel):
    name: str


weapon_router = fastapi.APIRouter(
    prefix="/weapons",
    tags=["weapons"],
    dependencies=[fastapi.Depends(db_dependencies.get_db_weapon_context)]
)


@weapon_router.post('/create')
async def create(
        weapon_post_model: WeaponPostModel,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    weapon_db_model = WeaponModel(**weapon_post_model.model_dump())
    try:
        await weapon_context.create(weapon_db_model)
    except IntegrityError:
        return {"success": False, "message": "Weapon with this name already exists, names need to be unique!"}
    await weapon_context.save_changes()
    return weapon_db_model


@weapon_router.get('/id/{id}')
async def get_weapon_by_id(
        id: int,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    if weapon_db_model := await weapon_context.get_by_id(id):
        return weapon_db_model
    else:
        return {"status": False, "message": f"Weapon with id - {str(id)!r} does not exist!"}


@weapon_router.put('/id/{id}')
async def update_weapon_by_id(
        id: int,
        weapon_post_model: WeaponPostModel,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    weapon_db_model = await weapon_context.get_by_id(id)
    if weapon_db_model is None:
        return {"status": False, "message": f"Weapon with id - {str(id)!r} does not exist!"}
    try:
        weapon_db_model.name = weapon_post_model.name
        await weapon_context.save_changes()
        return weapon_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Weapon with name {weapon_post_model.name!r} already exists, names need be unique!"}


@weapon_router.delete('/id/{id}')
async def delete_weapon_by_id(
        id: int,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    if await weapon_context.delete_by_id(id):
        await weapon_context.save_changes()
        return {'success': True, "message": f"Weapon with id - {str(id)!r} deleted"}
    return {"success": False, "message": f'Weapon with id - {str(id)!r} does not exist!'}


@weapon_router.get('/name/{name}')
async def get_weapon_by_name(
        name: str,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    if weapon_db_model := await weapon_context.get_by_name(name):
        return weapon_db_model
    else:
        return {"status": False, "message": f"Weapon with name - {name!r} does not exist!"}


@weapon_router.put('/name/{name}')
async def update_weapon_by_name(
        name: str,
        weapon_post_model: WeaponPostModel,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    weapon_db_model = await weapon_context.get_by_name(name)
    if weapon_db_model is None:
        return {"status": False, "message": f"Weapon with name - {name!r} does not exist!"}
    try:
        weapon_db_model.name = weapon_post_model.name
        await weapon_context.save_changes()
        return weapon_db_model
    except IntegrityError:
        return {"success": False,
                "message": f"Weapon with name {weapon_post_model.name!r} already exists, names need be unique!"}


@weapon_router.delete('/name/{name}')
async def delete_weapon_by_name(
        name: str,
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    if await weapon_context.delete_by_name(name):
        await weapon_context.save_changes()
        return {'success': True, "message": f"Weapon with name - {name!r} deleted"}
    return {"success": False, "message": f'Weapon with id - {name!r} does not exist!'}


@weapon_router.post('/create_many')
async def create_many(
        weapon_post_models: typing.List[WeaponPostModel],
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    weapon_db_models = [WeaponModel(**weapon_post_model.model_dump()) for weapon_post_model in weapon_post_models]
    try:
        await weapon_context.create_many(weapon_db_models)
    except IntegrityError:
        return {"success": False, "message": "Weapon names should be unique!"}
    await weapon_context.save_changes()
    return weapon_db_models


@weapon_router.get('/')
async def get_many(weapon_table: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)):
    return list(await weapon_table.get_all())


@weapon_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    existence_weapon_db_models = await weapon_context.get_many_by_id(ids)
    ids_on_delete = [weapon_db_model.id for weapon_db_model in existence_weapon_db_models]
    not_found_ids = [id for id in ids if id not in ids_on_delete]
    if ids_on_delete:
        await weapon_context.delete_many_by_id(ids_on_delete)
        await weapon_context.save_changes()
        return {
            'success': True,
            'message': f'Weapon with ids: {ids_on_delete} deleted. {f'{not_found_ids} not found' if not_found_ids else ''}'}
    return {"success": False, "message": f"Weapon with {ids} not found"}


@weapon_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        weapon_context: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)
):
    existence_weapon_db_models = await weapon_context.get_many_by_name(names)
    names_on_delete = [weapon_db_model.name for weapon_db_model in existence_weapon_db_models]
    not_found_names = [name for name in names if name not in names_on_delete]
    if names_on_delete:
        await weapon_context.delete_many_by_name(names_on_delete)
        await weapon_context.save_changes()
        return {
            'success': True,
            'message': f'Weapon with name {names_on_delete} deleted. {f'{not_found_names} not found' if not_found_names else ''}'
        }
    return {"success": False, "message": f"Weapon with names {names} not found"}


@weapon_router.get('/{name}/skins')
async def get_skins_for_weapon(name: str, weapon_table: WeaponContext = fastapi.Depends(db_dependencies.get_db_weapon_context)):
    return list(await weapon_table.get_skins_for_weapon(name))


