"""User endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.user.dependencies.user import get_path_user_id

from app.user.schemas.user import CreateUserSchema, UserSchema
from app.user.services.user import UserService
from app.user.schemas.user import UpdateUserSchema
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    AllowAll,
    IsAuthenticated,
    IsAdmin,
    IsUserOwner,
)
from core.versioning import version


user_v1_router = APIRouter()


@user_v1_router.get(
    "",
    response_model=list[UserSchema],
    dependencies=[Depends(PermissionDependency([[IsAdmin]]))],
)
@version(1)
async def get_users(session: Session = Depends(get_db)):
    return await UserService(session).get_users()


@user_v1_router.get(
    "/{user_id}",
    response_model=UserSchema,
    dependencies=[Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))],
)
@version(1)
async def get_user(user_id: str = Depends(get_path_user_id), session: Session = Depends(get_db)):
    return await UserService(session).get_user(user_id)


@user_v1_router.post(
    "",
    response_model=UserSchema,
    status_code=201,
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def create_user(schema: CreateUserSchema, session: Session = Depends(get_db)):
    return await UserService(session).create_user(schema)


@user_v1_router.patch(
    "/{user_id}",
    response_model=UserSchema,
    status_code=200,
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def update_user(
    schema: UpdateUserSchema, user_id: str = Depends(get_path_user_id), session: Session = Depends(get_db)
):
    return await UserService(session).update_user(user_id, schema)


@user_v1_router.delete(
    "/{user_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def delete_user(user_id: str = Depends(get_path_user_id), session: Session = Depends(get_db)):
    return await UserService(session).delete_user(user_id)
