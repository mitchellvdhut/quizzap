"""Question endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.question.schemas.question import CreateQuestionSchema, QuestionSchema, UpdateQuestionSchema
from app.question.services.question import QuestionService
from app.question.dependencies.question import get_path_question_id
from app.quiz.dependencies.quiz import get_path_quiz_id
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.permission.keyword import AND, OR
from core.fastapi.dependencies.permission.permissions import IsAdmin, IsAuthenticated, IsQuizOwner
from core.fastapi.dependencies.permission.permission_dependency import PermissionDependency
from core.versioning import version


question_v1_router = APIRouter()


@question_v1_router.get(
    "",
    response_model=list[QuestionSchema],
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_questions(
    quiz_id: int = Depends(get_path_quiz_id),
    session: Session = Depends(get_db),
):
    return await QuestionService(session).get_questions(quiz_id)


@question_v1_router.get(
    "/{question_id}",
    response_model=QuestionSchema,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_question(
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    session: Session = Depends(get_db),
):
    return await QuestionService(session).get_question(quiz_id, question_id)


@question_v1_router.post(
    "",
    response_model=QuestionSchema,
    status_code=201,
    dependencies=[Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))],
)
@version(1)
async def create_question(
    schema: CreateQuestionSchema,
    quiz_id: int = Depends(get_path_quiz_id),
    session: Session = Depends(get_db),
):
    return await QuestionService(session).create_question(quiz_id, schema)


@question_v1_router.patch(
    "/{question_id}",
    response_model=QuestionSchema,
    status_code=200,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def update_question(
    schema: UpdateQuestionSchema,
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    session: Session = Depends(get_db),
):
    return await QuestionService(session).update_question(quiz_id, question_id, schema)


@question_v1_router.delete(
    "/{question_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def delete_question(
    quiz_id: int = Depends(get_path_quiz_id),
    question_id: int = Depends(get_path_question_id),
    session: Session = Depends(get_db),
):
    return await QuestionService(session).delete_question(quiz_id, question_id, question_id)
