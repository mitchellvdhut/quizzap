from sqlalchemy.orm import Session
from core.db.models import Answer
from core.repository.base import BaseRepository


class AnswerRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Answer, session)
