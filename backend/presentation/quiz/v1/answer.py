"""Answer endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.answer.schemas.answer import CreateAnswerSchema, AnswerSchema, UpdateAnswerSchema
from app.answer.services.answer import AnswerService
from app.answer.dependencies.answer import get_path_answer_id
from app.question.dependencies.question import get_path_question_id
from app.quiz.dependencies.quiz import get_path_quiz_id
from core.fastapi.dependencies.permission.keyword import AND, OR
from core.fastapi.dependencies.permission.permissions import IsAdmin, IsAuthenticated, IsQuizOwner
from core.fastapi.dependencies.permission.permission_dependency import PermissionDependency
from core.fastapi.dependencies.database import get_db
from core.versioning import version


answer_v1_router = APIRouter()


@answer_v1_router.get(
    "",
    response_model=list[AnswerSchema],
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_answers(
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    session: Session = Depends(get_db),
):
    return await AnswerService(session).get_answers(quiz_id, question_id)


@answer_v1_router.get(
    "/{answer_id}",
    response_model=AnswerSchema,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_answer(
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    answer_id: int = Depends(get_path_answer_id),
    session: Session = Depends(get_db),
):
    return await AnswerService(session).get_answer(quiz_id, question_id, answer_id)


@answer_v1_router.post(
    "",
    response_model=AnswerSchema,
    status_code=201,
    dependencies=[Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))],
)
@version(1)
async def create_answer(
    schema: CreateAnswerSchema,
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    session: Session = Depends(get_db),
):
    return await AnswerService(session).create_answer(quiz_id, question_id, schema)


@answer_v1_router.patch(
    "/{answer_id}",
    response_model=AnswerSchema,
    status_code=200,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def update_answer(
    schema: UpdateAnswerSchema,
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    answer_id: int = Depends(get_path_answer_id),
    session: Session = Depends(get_db),
):
    return await AnswerService(session).update_answer(quiz_id, question_id, answer_id, schema)


@answer_v1_router.delete(
    "/{answer_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def delete_answer(
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    answer_id: int = Depends(get_path_answer_id),
    session: Session = Depends(get_db),
):
    return await AnswerService(session).delete_answer(quiz_id, question_id, answer_id)
