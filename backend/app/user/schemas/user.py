from datetime import datetime
from pydantic import ConfigDict, BaseModel

from core.schemas.hashids import HashId


class CreateUserSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: HashId
    username: str
    password: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    username: str
    password: str = None
