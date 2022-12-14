from sqlalchemy.future import select
from models.user_model import UserModel

from utils.database import AsyncSession


async def get_user_by_email(db: AsyncSession, email: str) -> UserModel | None:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        return result.scalar()


async def create_user(db: AsyncSession, user: UserModel) -> UserModel:
    async with db as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
