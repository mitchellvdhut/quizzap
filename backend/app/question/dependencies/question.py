from fastapi import Path
from core.helpers.hashids import decode_single


async def get_path_question_id(question_id: str = Path(...)):
    return decode_single(question_id)
