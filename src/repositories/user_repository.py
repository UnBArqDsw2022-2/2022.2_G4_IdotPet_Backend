from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select

from models import BaseUserModel, OngUserModel, UserModel
from utils.database import AsyncSession, get_db

from .base_repository import BaseRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseUserRepository(BaseRepository):
    def __init__(self, model_class: type[UserModel | OngUserModel], db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(model_class, db)

    async def create(self, model: BaseUserModel) -> BaseUserModel:
        model.password = pwd_context.hash(model.password)  # type: ignore
        return await super().create(model)

    async def get_user_by_email(self, email: str) -> BaseUserModel | None:
        query = select(BaseUserModel).filter(BaseUserModel.email == email)
        result = await self.db.execute(query)
        return result.scalar()

    async def verify_user_password(self, email: str, password: str) -> int:
        query = select(BaseUserModel).filter(BaseUserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar()

        if not user or not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user.id
