from datetime import datetime
from pydantic import ConfigDict, BaseModel


class CreateAnswerSchema(BaseModel):
    description: str


class AnswerSchema(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateAnswerSchema(BaseModel):
    description: str
