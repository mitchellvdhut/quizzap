"""
Base reposity to contain crud logic
"""

from typing import TypeVar, Type, Optional, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from core.db import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    """
    A generic repository that provides basic database operations for a given SQLAlchemy 
    model.
    """

    def __init__(self, model: Type[Model], session: Session):
        self.model = model
        self.session = session
    
    def query_options(self, query):
        return query
    
    def get(self) -> Optional[list[Model]]:
        query = select(self.model)
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all()

    def get_by_id(self, model_id: int) -> Optional[Model]:
        query = select(self.model).where(self.model.id == model_id)
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()

    def update_by_id(
        self,
        model_id: int,
        params: dict,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**params)
        )
        query = self.query_options(query)
        self.session.execute(query)
        self.session.commit()

    def delete(self, model: Model) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(
        self,
        model_id: int,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == model_id)
        )
        self.session.execute(query)
        self.session.commit()

    def create(self, model: Model) -> int:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
