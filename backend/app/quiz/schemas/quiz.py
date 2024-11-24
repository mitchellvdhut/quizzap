from datetime import datetime
from pydantic import ConfigDict, BaseModel

from app.question.schemas.question import QuestionSchema, UploadQuestionSchema
from app.user.schemas.user import UserSchema
from core.schemas.hashids import DehashId, HashId


class CreateQuizSchema(BaseModel):
    name: str
    description: str


class UploadQuizSchema(BaseModel):
    id: DehashId | None = None
    name: str
    description: str

    questions: list[UploadQuestionSchema]


class QuizSchema(BaseModel):
    id: HashId
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    creator: UserSchema

    questions: list[QuestionSchema]

    model_config = ConfigDict(from_attributes=True)


class UpdateQuizSchema(BaseModel):
    name: str
    description: str
