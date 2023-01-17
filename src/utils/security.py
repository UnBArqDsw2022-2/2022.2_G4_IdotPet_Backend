from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models import BaseUserModel, OngUserModel, UserModel
from repositories import repository_factory
from utils.database import AsyncSession, get_db
from utils.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def generate_token(user_id: int) -> str:
    issued_at = datetime.utcnow()
    expires = issued_at + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({
        'exp': int(expires.timestamp()),
        'sub': str(user_id),
        'iat': int(issued_at.timestamp()),
        'iss': 'IdotPet'
    }, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, key=settings.JWT_SECRET,
                             algorithms=settings.JWT_ALGORITHM)
        return int(payload['sub'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def logged_user(id_: int = Depends(decode_token), db: AsyncSession = Depends(get_db)) -> UserModel | OngUserModel:
    try:
        repository = await repository_factory(BaseUserModel, db)
        return await repository.get_by_id(id_)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
