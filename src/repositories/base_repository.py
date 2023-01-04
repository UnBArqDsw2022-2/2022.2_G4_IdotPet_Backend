from fastapi import Depends
from typing import Generic, TypeVar

from sqlalchemy import select

from utils.database import AsyncSession, Base, get_db

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: type[T], db: AsyncSession = Depends(get_db)) -> None:
        self.model_class = model_class
        self.db = db

    async def create(self, model: T) -> T:
        async with self.db as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
        return model

    async def get_by_id(self, id_: int) -> T | None:
        async with self.db as session:
            query = select(self.model_class).filter(self.model_class.id == id_)
            result = await session.execute(query)
            return result.scalar()

    async def get_all(self) -> list[T]:
        async with self.db as session:
            query = select(self.model_class).order_by(self.model_class.id)
            result = await session.execute(query)
            return result.scalars().all()

    async def update(self, model: T) -> T:
        to_update = await self.get_by_id(model.id)
        if not to_update:
            raise

        body = model.dict()
        for key, value in body.items():
            if value is None:
                continue

            setattr(to_update, key, value)

        async with self.db as session:
            await session.merge(to_update)
            await session.commit()
            await session.refresh(to_update)

        return to_update

    async def delete(self, model: T) -> T:
        to_delete = await self.get_by_id(model.id)
        if not to_delete:
            raise 

        async with self.db as session:
            await session.delete(to_delete)
            await session.commit()

        return to_delete
