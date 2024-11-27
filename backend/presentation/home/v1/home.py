"""Home endpoints."""

from fastapi import APIRouter, Depends, Response
from core.fastapi.dependencies.permission.permission_dependency import PermissionDependency
from core.fastapi.dependencies.permission.permissions import AllowAll
from core.versioning import version


home_v1_router = APIRouter()


@home_v1_router.get(
    "/health",
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def health():
    return Response(status_code=200)
