from datetime import datetime
from pydantic import ConfigDict, BaseModel

from app.answer.schemas.answer import AnswerSchema, UploadAnswerSchema
from core.schemas.hashids import HashId


class CreateQuestionSchema(BaseModel):
    name: str
    description: str
    time_limit: float = 30.0


class UploadQuestionSchema(BaseModel):
    name: str
    description: str
    time_limit: float = 30.0

    answers: list[UploadAnswerSchema]


class QuestionSchema(BaseModel):
    id: HashId
    name: str
    description: str
    time_limit: float
    created_at: datetime
    updated_at: datetime

    answers: list[AnswerSchema]

    model_config = ConfigDict(from_attributes=True)


class UpdateQuestionSchema(BaseModel):
    name: str
    description: str
    time_limit: float = 30.0
