from fastapi import Path, Request

from core.config import config
from core.enums.internal import Modes
from core.db.models import User
from core.helpers.hashids import decode_single


async def get_current_user(request: Request) -> User:
    user = request.user

    if not user or not user.id:
        if config.MODE == Modes.ANARCHY.value:
            return 1
        
        return None
    
    return user.id

async def get_path_user_id(user_id: str = Path(...)):
    return decode_single(user_id)
