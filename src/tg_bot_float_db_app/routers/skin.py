import typing

import fastapi
from sqlalchemy.exc import IntegrityError

from tg_bot_float_db_app.database.contexts.skin import SkinContext
from tg_bot_float_db_app.dependencies import db_dependencies
from tg_bot_float_db_app.database.models.skin_models import SkinModel
from tg_bot_float_db_app.misc.post_models import SkinPostModel
from tg_bot_float_db_app.misc.msg_response_dto import MsgResponseDTO

skin_router = fastapi.APIRouter(
    prefix="/skins",
    tags=["skins"])


@skin_router.post("/create")
async def create(
        skin_post_model: SkinPostModel,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = SkinModel(**skin_post_model.model_dump())
    try:
        await skin_context.create(skin_db_model)
    except IntegrityError:
        return MsgResponseDTO(status=False, msg="Skin with this name already exists, names need to be unique!")
    await skin_context.save_changes()
    return skin_db_model


@skin_router.get("/id/{skin_id}")
async def get_skin_by_id(
        skin_id: int,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if skin_db_model := await skin_context.get_by_id(skin_id):
        return skin_db_model
    else:
        return MsgResponseDTO(status=False, msg=f"Skin with id - {str(skin_id)!r} does not exist!")


@skin_router.put("/id/{skin_id}")
async def update_skin_by_id(
        skin_id: int,
        skin_post_model: SkinPostModel,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = await skin_context.get_by_id(skin_id)
    if skin_db_model is None:
        return MsgResponseDTO(status=False, msg=f"Skin with id - {str(skin_id)!r} does not exist!")
    try:
        skin_db_model.name = skin_post_model.name
        skin_db_model.stattrak_existence = skin_post_model.stattrak_existence
        await skin_context.save_changes()
        return skin_db_model
    except IntegrityError:
        return MsgResponseDTO(
            status=False, msg=f"Weapon with name {skin_post_model.name!r} already exists, names need be unique!")


@skin_router.delete("/id/{skin_id}")
async def delete_skin_by_id(
        skin_id: int,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if await skin_context.delete_by_id(skin_id):
        await skin_context.save_changes()
        return MsgResponseDTO(status=True, msg=f"Skin with id - {str(skin_id)!r} deleted")
    return MsgResponseDTO(status=False, msg=f'Skin with id - {str(skin_id)!r} does not exist!')


@skin_router.get('/name/{name}')
async def get_skin_by_name(
        name: str,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if skin_db_model := await skin_context.get_by_name(name):
        return skin_db_model
    else:
        return MsgResponseDTO(status=False, msg=f"Skin with name - {name!r} does not exist!")


@skin_router.put('/name/{name')
async def update_skin_by_name(
        name: str,
        skin_post_model: SkinPostModel,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    skin_db_model = await skin_context.get_by_name(name)
    if skin_db_model is None:
        return MsgResponseDTO(status=False, msg=f"Skin with name - {name!r} does not exist!")
    try:
        skin_db_model.name = skin_post_model.name
        skin_db_model.stattrak_existence = skin_post_model.stattrak_existence
        await skin_context.save_changes()
        return skin_db_model
    except IntegrityError:
        return MsgResponseDTO(
            status=False,
            msg=f"Skin with name {skin_post_model.name!r} already exists, names need be unique!")


@skin_router.delete('/name/{name}')
async def delete_skin_by_name(
        name: str,
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    if await skin_context.delete_by_name(name):
        await skin_context.save_changes()
        return MsgResponseDTO(status=True, msg=f"Skin with name - {name!r} deleted")
    return MsgResponseDTO(status=False, msg=f'Skin with id - {name!r} does not exist!')


@skin_router.post('/create_many')
async def create_many(
        skin_post_models: typing.List[SkinPostModel],
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    weapon_db_models = [SkinModel(**skin_post_model.model_dump()) for skin_post_model in skin_post_models]
    try:
        await skin_context.create_many(weapon_db_models)
    except IntegrityError:
        return MsgResponseDTO(status=False, msg="Skin names should be unique!")
    await skin_context.save_changes()
    return weapon_db_models

@skin_router.get('/')
async def get_many(skin_table: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)):
    return list(await skin_table.get_all())


@skin_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    existence_skin_db_models = await skin_context.get_many_by_id(ids)
    ids_on_delete = [skin_db_model.id for skin_db_model in existence_skin_db_models]
    not_found_ids = [id for id in ids if id not in ids_on_delete]
    if ids_on_delete:
        await skin_context.delete_many_by_id(ids_on_delete)
        await skin_context.save_changes()
        return MsgResponseDTO(
            status=True,
            msg=f'Skin with ids: {ids_on_delete} deleted. {f'{not_found_ids} not found' if not_found_ids else ''}')
    return MsgResponseDTO(status=False, msg=f"Skin with {ids} not found")


@skin_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        skin_context: SkinContext = fastapi.Depends(db_dependencies.get_db_skin_context)
):
    existence_skin_db_models = await skin_context.get_many_by_name(names)
    names_on_delete = [skin_db_model.name for skin_db_model in existence_skin_db_models]
    not_found_names = [name for name in names if name not in names_on_delete]
    if names_on_delete:
        await skin_context.delete_many_by_name(names_on_delete)
        await skin_context.save_changes()
        return MsgResponseDTO(
            status=True,
            msg=f'Skin with name {names_on_delete} deleted. {f'{not_found_names} not found' if not_found_names else ''}')
    return MsgResponseDTO(status=False, msg=f"Skin with names {names} not found")
