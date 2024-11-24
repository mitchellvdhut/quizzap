from app.quiz.schemas.quiz import CreateQuizSchema, UpdateQuizSchema
from app.quiz.exceptions.quiz import DuplicateNameException, QuizNotFoundException
from app.quiz.repository.quiz import QuizRepository
from core.db.models import Quiz


class QuizService:
    def __init__(self, session) -> None:
        self.repo = QuizRepository(session)

    async def get_by_name(self, name):
        return self.repo.get_by_name(name)

    async def create_quiz(self, schema: CreateQuizSchema, current_user: int):
        quiz = self.repo.get_by_name(schema.name)

        if quiz:
            raise DuplicateNameException

        quiz = Quiz(
            name=schema.name,
            description=schema.description,
            created_by=current_user,
        )
        return self.repo.create(quiz)

    async def delete_quiz(self, quiz_id: int) -> None:
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        self.repo.delete(quiz)

    async def update_quiz(self, quiz_id: int, schema: UpdateQuizSchema):
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        params = {"name": schema.name, "description": schema.description}

        self.repo.update_by_id(quiz_id, params)
        return self.repo.get_by_id(quiz_id)

    async def get_quiz(self, quiz_id: int):
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        return quiz

    async def get_quizzes(self):
        return self.repo.get()

    async def is_admin(self, quiz_id):
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        return quiz.is_admin
