from fastapi import Path, Request

from core.db.models import User
from core.helpers.hashids import decode_single


async def get_current_user(request: Request) -> User:
    user = request.user
    if not user or not user.id:
        return None
    
    return user.id

async def get_path_user_id(user_id: str = Path(...)):
    return decode_single(user_id)
