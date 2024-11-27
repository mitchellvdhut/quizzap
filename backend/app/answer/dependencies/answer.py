from fastapi import Path
from core.helpers.hashids import decode_single


async def get_path_answer_id(answer_id: str = Path(...)):
    return decode_single(answer_id)
