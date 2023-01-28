from typing import Any, Generic, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import with_polymorphic

from utils.database import AsyncSession, Base, get_db

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: type[ModelType], db: AsyncSession = Depends(get_db)) -> None:
        self.model_class = with_polymorphic(model_class, "*")
        self.db = db

    async def create(self, model: ModelType) -> ModelType:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def create_all(self, models: list[ModelType]) -> list[ModelType]:
        for model in models:
            self.db.add(model)
        await self.db.commit()

        for model in models:
            await self.db.refresh(model)
        return models

    async def get_by_id(self, id_: int) -> ModelType:
        query = select(self.model_class).filter(self.model_class.id == id_)
        result = await self.db.execute(query)
        model = result.scalar()
        if not model:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{self.model_class.__name__.rstrip("Model").lstrip("AliasedClass_").lstrip("Base")} not found')
        return model

    async def get_all(self, filters: dict[str, Any] | None = None) -> list[ModelType]:
        if filters == None:
            filters = {}

        query = select(self.model_class).filter_by(**filters).order_by(self.model_class.id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, model: ModelType) -> ModelType:
        await self.db.merge(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model

    async def delete(self, model: ModelType) -> ModelType:
        await self.db.delete(model)
        await self.db.commit()

        return model

    async def delete_all(self, models: list[ModelType]) -> list[ModelType]:
        for model in models:
            await self.db.delete(model)
        await self.db.commit()

        return models
