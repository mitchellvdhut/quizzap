from datetime import datetime
from typing import TypedDict

from core.db.models import Question, Quiz


class PoolData(TypedDict):
    quiz: Quiz
    question: Question
    question_index: int
    question_start: datetime | None
    question_stop: datetime | None
    is_stopping: datetime | None
    question_active: bool


class UserScore(TypedDict):
    username: str
    score: int
    streak: int


class UserData(TypedDict):
    username: str
    vote: int | None
    voted_at: datetime | None
    is_admin: bool | None
    score: int
    streak: int
    is_player: bool
