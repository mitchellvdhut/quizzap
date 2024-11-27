from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.user.dependencies.user import get_current_user
from app.user.services.user import UserService
from app.user.schemas.user import FullUserSchema, UpdateUserSchema
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.permission.permission_dependency import PermissionDependency
from core.fastapi.dependencies.permission.permissions import IsAuthenticated
from core.versioning import version


me_v1_router = APIRouter()


@me_v1_router.get(
    "",
    response_model=FullUserSchema,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_me(
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return await UserService(session=session).get_user(user_id)


@me_v1_router.patch(
    "",
    response_model=FullUserSchema,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def update_me(
    schema: UpdateUserSchema,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return await UserService(session=session).update_user(user_id, schema)


@me_v1_router.delete(
    "",
    status_code=204,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def delete_me(
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return await UserService(session).delete_user(user_id)
