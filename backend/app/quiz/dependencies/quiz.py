import logging
from fastapi import Path
from core.exceptions.hashids import IncorrectHashIDException
from core.helpers.hashids import decode_single


async def get_path_quiz_id(quiz_id: str = Path(...)):
    try:
        return decode_single(quiz_id)
    
    except IncorrectHashIDException:
        logger = logging.getLogger("quizzap")
        logger.error("Incorrect hash, can't really smoke this.")
