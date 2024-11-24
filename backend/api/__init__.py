"""Bundle all endpoints."""

from fastapi import APIRouter

from api.home.v1.home import home_v1_router
from api.user.v1.user import user_v1_router
from api.auth.v1.auth import auth_v1_router
from api.me.v1.me import me_v1_router


router = APIRouter()
router.include_router(home_v1_router, prefix="", tags=["Home"])
router.include_router(auth_v1_router, prefix="/auth", tags=["Auth"])
router.include_router(user_v1_router, prefix="/users", tags=["Users"])
router.include_router(me_v1_router, prefix="/me", tags=["Me"])


__all__ = ["router"]
