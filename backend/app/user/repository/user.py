from sqlalchemy import select
from sqlalchemy.orm import Session
from core.db.models import User
from core.repository.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str):
        query = select(self.model).where(self.model.username==username)
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()
