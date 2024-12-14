from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from core.db.models import Question, Quiz
from core.repository.base import BaseRepository


class QuizRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Quiz, session)

    def get_by_id_loaded(self, model_id: int) -> Optional[Quiz]:
        query = (
            select(self.model)
            .options(selectinload(Quiz.questions)
                     .selectinload(Question.answers))
            .where(self.model.id == model_id)
        )
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()

    def get_by_name(self, name: str) -> Optional[Quiz]:
        query = select(self.model).where(self.model.name == name)
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()
