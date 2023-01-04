from fastapi import Depends
from sqlalchemy import select

from models.user_model import UserModel
from utils.database import AsyncSession, get_db
from utils.security import pwd_context

from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(UserModel, db)

    async def create(self, model: UserModel) -> UserModel:
        model.password = pwd_context.hash(model.password)  # type: ignore
        return await super().create(model)

    async def get_user_by_email(self, email) -> UserModel | None:
        async with self.db as session:
            query = select(UserModel).filter(UserModel.email == email)
            result = await session.execute(query)
            return result.scalar()
