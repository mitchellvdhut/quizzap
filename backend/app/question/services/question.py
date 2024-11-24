from app.question.schemas.question import CreateQuestionSchema, UpdateQuestionSchema
from app.question.exceptions.question import QuestionNotFoundException
from app.question.repository.question import QuestionRepository
from app.quiz.services.quiz import QuizService
from core.db.models import Question


class QuestionService:
    def __init__(self, session) -> None:
        self.repo = QuestionRepository(session)
        self.quiz_serv = QuizService(session)

    async def create_question(self, quiz_id: int, schema: CreateQuestionSchema) -> Question:
        await self.quiz_serv.get_quiz(quiz_id)

        question = Question(name=schema.name, description=schema.description)
        return self.repo.create(question)

    async def delete_question(self, quiz_id: int, question_id: int) -> None:
        await self.quiz_serv.get_quiz(quiz_id)

        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        self.repo.delete(question)

    async def update_question(self, quiz_id: int, question_id: int, schema: UpdateQuestionSchema) -> Question:
        await self.quiz_serv.get_quiz(quiz_id)
        
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        params = {"name": schema.name, "description": schema.description}
        
        self.repo.update_by_id(question_id, params)
        return self.repo.get_by_id(question_id)
    
    async def get_question(self, quiz_id: int, question_id: int) -> Question:
        await self.quiz_serv.get_quiz(quiz_id)
        
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException
        
        return question
    
    async def get_questions(self, quiz_id: int) -> list[Question]:
        quiz = await self.quiz_serv.get_quiz(quiz_id)
        
        return quiz.questions
