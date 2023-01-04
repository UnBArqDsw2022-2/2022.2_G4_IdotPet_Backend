from typing import Generic, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from utils.database import AsyncSession, Base, get_db

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: type[T], db: AsyncSession = Depends(get_db)) -> None:
        self.model_class = model_class
        self.db = db

    async def create(self, model: T) -> T:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def get_by_id(self, id_: int) -> T:
        query = select(self.model_class).filter(self.model_class.id == id_)
        result = await self.db.execute(query)
        model = result.scalar()
        if not model:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                detail=f'{self.model_class.__name__.rstrip("Model")} not found')
        return model

    async def get_all(self) -> list[T]:
        query = select(self.model_class).order_by(self.model_class.id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, model: T) -> T:
        to_update = await self.get_by_id(model.id)

        await self.db.merge(to_update)
        await self.db.commit()
        await self.db.refresh(to_update)

        return to_update

    async def delete(self, model: T) -> T:
        to_delete = await self.get_by_id(model.id)

        await self.db.delete(to_delete)
        await self.db.commit()

        return to_delete
