from sqlalchemy import select
from sqlalchemy.orm import Session
from core.db.models import Question
from core.repository.base import BaseRepository


class QuestionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Question, session)

    def get_by_name(self, name: str):
        query = select(self.model).where(self.model.name==name)
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()
