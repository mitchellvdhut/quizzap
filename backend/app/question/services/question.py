from app.question.schemas.question import CreateQuestionSchema, UpdateQuestionSchema
from app.question.exceptions.question import DuplicateNameException, QuestionNotFoundException
from app.question.repository.question import QuestionRepository
from core.db.models import Question


class QuestionService:
    def __init__(self, session) -> None:
        self.repo = QuestionRepository(session)

    async def get_by_name(self, name):
        return self.repo.get_by_name(name)

    async def create_question(self, schema: CreateQuestionSchema):
        question = self.repo.get_by_name(schema.name)

        if question:
            raise DuplicateNameException

        question = Question(name=schema.name, description=schema.description)
        return self.repo.create(question)

    async def delete_question(self, question_id: int) -> None:
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        self.repo.delete(question)

    async def update_question(self, question_id: int, schema: UpdateQuestionSchema):
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        params = {"name": schema.name, "description": schema.description}
        
        self.repo.update_by_id(question_id, params)
        return self.repo.get_by_id(question_id)
    
    async def get_question(self, question_id: int):
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        return question
    
    async def get_questionzes(self):
        return self.repo.get()
    
    async def is_admin(self, question_id):
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        return question.is_admin

