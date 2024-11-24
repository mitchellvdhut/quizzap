"""
Module to encode and decode integers.
"""

from hashids import Hashids

from core.config import config
from core.exceptions.hashids import IncorrectHashIDException

hashids = Hashids(salt=config.HASH_ID_SALT, min_length=config.HASH_ID_MIN_LENGTH)


def encode(id_to_hash):
    """Hashids encode function"""
    return hashids.encode(id_to_hash)


def decode(hashed_ids):
    """Hashids decode function"""
    try:
        return hashids.decode(hashed_ids)

    except Exception as exc:
        raise IncorrectHashIDException from exc


def decode_single(hashed_ids) -> int:
    """Decode, return single ID"""
    real_ids = ()

    real_ids = decode(hashed_ids)

    if len(real_ids) < 1:
        raise IncorrectHashIDException

    return real_ids[0]
