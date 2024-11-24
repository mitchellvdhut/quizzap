from fastapi import Path
from core.helpers.hashids import decode_single


async def get_path_quiz_id(quiz_id: str = Path(...)):
    return decode_single(quiz_id)
