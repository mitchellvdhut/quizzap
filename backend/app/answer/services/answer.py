from app.answer.schemas.answer import CreateAnswerSchema, UpdateAnswerSchema
from app.answer.exceptions.answer import AnswerNotFoundException
from app.answer.repository.answer import AnswerRepository
from app.question.services.question import QuestionService
from app.quiz.services.quiz import QuizService
from core.db.models import Answer


class AnswerService:
    def __init__(self, session) -> None:
        self.repo = AnswerRepository(session)
        self.quiz_serv = QuizService(session)
        self.question_serv = QuestionService(session)

    async def create_answer(
        self,
        quiz_id: int,
        question_id: int,
        schema: CreateAnswerSchema,
    ) -> Answer:
        await self.question_serv.get_question(quiz_id, question_id)

        answer = Answer(
            description=schema.description,
            is_correct=schema.is_correct,
        )
        return self.repo.create(answer)

    async def delete_answer(
        self,
        quiz_id: int,
        question_id: int,
        answer_id: int,
    ) -> None:
        await self.question_serv.get_question(quiz_id, question_id)

        answer = self.repo.get_by_id(answer_id)
        if not answer:
            raise AnswerNotFoundException

        self.repo.delete(answer)

    async def update_answer(
        self,
        quiz_id: int,
        question_id: int,
        answer_id: int,
        schema: UpdateAnswerSchema,
    ) -> Answer:
        await self.question_serv.get_question(quiz_id, question_id)

        answer = self.repo.get_by_id(answer_id)
        if not answer:
            raise AnswerNotFoundException

        params = {
            "is_correct": schema.is_correct,
            "description": schema.description,
        }

        self.repo.update_by_id(answer_id, params)
        return self.repo.get_by_id(answer_id)

    async def get_answer(
        self,
        quiz_id: int,
        question_id: int,
        answer_id: int,
    ) -> Answer:
        await self.question_serv.get_question(quiz_id, question_id)

        answer = self.repo.get_by_id(answer_id)
        if not answer:
            raise AnswerNotFoundException

        return answer

    async def get_answers(
        self,
        quiz_id: int,
        question_id: int,
    ) -> list[Answer]:
        question = await self.question_serv.get_question(quiz_id, question_id)

        return question.answers
