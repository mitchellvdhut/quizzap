"""Database models."""


from sqlalchemy import (
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    quizzes: Mapped[list["Quiz"]] = relationship(
        back_populates="creator", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"User('{self.username}')"


class Quiz(Base, TimestampMixin):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))

    creator: Mapped[User] = relationship(back_populates="quizzes")

    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", cascade="all, delete"
    )


class Question(Base, TimestampMixin):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    time_limit: Mapped[float] = mapped_column(default=30.0)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))

    quiz: Mapped[Quiz] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question", cascade="all, delete"
    )


class Answer(Base, TimestampMixin):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))

    question: Mapped[Question] = relationship(back_populates="answers")
