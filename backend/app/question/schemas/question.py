from datetime import datetime
from pydantic import ConfigDict, BaseModel


class CreateQuestionSchema(BaseModel):
    name: str
    description: str


class QuestionSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateQuestionSchema(BaseModel):
    name: str
    description: str
