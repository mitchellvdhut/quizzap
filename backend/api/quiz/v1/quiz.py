"""Quiz endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.quiz.dependencies.quiz import get_path_quiz_id

from app.quiz.schemas.quiz import CreateQuizSchema, QuizSchema
from app.quiz.services.quiz import QuizService
from app.quiz.schemas.quiz import UpdateQuizSchema
from app.user.dependencies.user import get_current_user
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    # AllowAll,
    IsAuthenticated,
    IsAdmin,
    IsQuizOwner,
    AND,
    OR,
)
from core.versioning import version


quiz_v1_router = APIRouter()


@quiz_v1_router.get(
    "",
    response_model=list[QuizSchema],
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_quizzes(session: Session = Depends(get_db)):
    return await QuizService(session).get_quizzes()


@quiz_v1_router.get(
    "/{quiz_id}",
    response_model=QuizSchema,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def get_quiz(
    quiz_id: str = Depends(get_path_quiz_id),
    session: Session = Depends(get_db),
):
    return await QuizService(session).get_quiz(quiz_id)


@quiz_v1_router.post(
    "",
    response_model=QuizSchema,
    status_code=201,
    dependencies=[Depends(PermissionDependency(IsAuthenticated))],
)
@version(1)
async def create_quiz(
    schema: CreateQuizSchema,
    session: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await QuizService(session).create_quiz(schema, current_user)


@quiz_v1_router.patch(
    "/{quiz_id}",
    response_model=QuizSchema,
    status_code=200,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def update_quiz(
    schema: UpdateQuizSchema,
    quiz_id: str = Depends(get_path_quiz_id),
    session: Session = Depends(get_db),
):
    return await QuizService(session).update_quiz(quiz_id, schema)


@quiz_v1_router.delete(
    "/{quiz_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency(IsAdmin, OR, (IsAuthenticated, AND, IsQuizOwner)))
    ],
)
@version(1)
async def delete_quiz(
    quiz_id: str = Depends(get_path_quiz_id),
    session: Session = Depends(get_db),
):
    return await QuizService(session).delete_quiz(quiz_id)
