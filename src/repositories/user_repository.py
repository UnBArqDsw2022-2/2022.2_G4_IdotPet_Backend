from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select

from models.user_model import UserModel
from utils.database import AsyncSession, get_db

from .base_repository import BaseRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(UserModel, db)

    async def create(self, model: UserModel) -> UserModel:
        model.password = pwd_context.hash(model.password)  # type: ignore
        return await super().create(model)

    async def get_user_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).filter(UserModel.email == email)
        result = await self.db.execute(query)
        return result.scalar()

    async def verify_user_password(self, email: str, password: str) -> int:
        query = select(UserModel).filter(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar()

        if not user or not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user.id
