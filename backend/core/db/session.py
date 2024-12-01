from core.db import SessionLocal


def get_session(func):
    def wrapper(*args, **kwagrs):
        with SessionLocal() as session:
            return func(session, *args, **kwagrs)
    return wrapper
