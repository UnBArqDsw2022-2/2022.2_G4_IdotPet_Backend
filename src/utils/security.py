from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from utils.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token(user_id: int) -> str:
    issued_at = datetime.utcnow()
    expires = issued_at + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({
        'exp': int(expires.timestamp()),
        'sub': user_id,
        'iat': int(issued_at.timestamp()),
        'iss': 'IdotPet'
    }, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
