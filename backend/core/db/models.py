"""Database models."""


from sqlalchemy import (
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)


    def __repr__(self) -> str:
        return f"User('{self.username}')"
