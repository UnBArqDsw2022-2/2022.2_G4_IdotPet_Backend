from utils.database import AsyncSession

import models
from .base_repository import BaseRepository, ModelType
from .user_repository import BaseUserRepository


async def repository_factory(model_class: type[ModelType], db: AsyncSession) -> BaseRepository[ModelType]:
    if issubclass(model_class, models.BaseUserModel):
        return BaseUserRepository(model_class, db)

    return BaseRepository(model_class, db)
