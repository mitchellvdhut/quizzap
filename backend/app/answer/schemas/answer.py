from datetime import datetime
from pydantic import ConfigDict, BaseModel

from core.schemas.hashids import HashId


class CreateAnswerSchema(BaseModel):
    description: str
    is_correct: bool = False


class UploadAnswerSchema(BaseModel):
    description: str
    is_correct: bool


class AnswerSchema(BaseModel):
    id: HashId
    description: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateAnswerSchema(BaseModel):
    description: str
    is_correct: bool = False
