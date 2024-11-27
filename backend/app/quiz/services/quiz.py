from app.quiz.schemas.quiz import CreateQuizSchema, UpdateQuizSchema, UploadQuizSchema
from app.quiz.exceptions.quiz import DuplicateNameException, QuizNotFoundException
from app.quiz.repository.quiz import QuizRepository
from core.db.models import Answer, Question, Quiz


class QuizService:
    def __init__(self, session) -> None:
        self.repo = QuizRepository(session)

    async def upload_quiz(
        self,
        schema: UploadQuizSchema,
        current_user: int,
    ) -> Quiz:
        quiz = self.repo.get_by_name(schema.name)

        if quiz and quiz.id != schema.id:
            raise DuplicateNameException

        else:
            quiz = Quiz()

        quiz.name = schema.name
        quiz.description = schema.description
        quiz.created_by = current_user

        quiz.questions = []

        for question in schema.questions:
            new_question = Question(
                name=question.name,
                description=question.description,
            )

            for answer in question.answers:
                new_answer = Answer(
                    description=answer.description, is_correct=answer.is_correct
                )

                new_question.answers.append(new_answer)

            quiz.questions.append(new_question)

        self.repo.session.add(quiz)
        self.repo.session.commit()
        self.repo.session.refresh(quiz)

        return quiz

    async def get_by_name(self, name) -> Quiz:
        return self.repo.get_by_name(name)

    async def create_quiz(
        self,
        schema: CreateQuizSchema,
        current_user: int,
    ) -> Quiz:
        quiz = self.repo.get_by_name(schema.name)

        if quiz:
            raise DuplicateNameException

        quiz = Quiz(
            name=schema.name,
            description=schema.description,
            created_by=current_user,
        )
        return self.repo.create(quiz)

    async def delete_quiz(
        self,
        quiz_id: int,
    ) -> None:
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        self.repo.delete(quiz)

    async def update_quiz(
        self,
        quiz_id: int,
        schema: UpdateQuizSchema,
    ) -> Quiz:
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        params = {
            "name": schema.name,
            "description": schema.description,
        }

        self.repo.update_by_id(quiz_id, params)
        return self.repo.get_by_id(quiz_id)

    async def get_quiz(
        self,
        quiz_id: int,
    ) -> Quiz:
        quiz = self.repo.get_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException

        return quiz

    async def get_quizzes(self) -> list[Quiz]:
        return self.repo.get()
