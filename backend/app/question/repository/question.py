from sqlalchemy.orm import Session
from core.db.models import Question
from core.repository.base import BaseRepository


class QuestionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Question, session)
