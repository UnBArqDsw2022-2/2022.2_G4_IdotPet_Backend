from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from repositories import user_repository
from utils.database import AsyncSession, get_db
from utils.security import generate_token, pwd_context
from views.user_view import UserCreate, UserView

router = APIRouter(prefix='/user', tags=['Usuário'])


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_email(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {'access_token': generate_token(user.id_user), 'token_type': 'bearer'}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserView)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Validate email and cpf
    #   Check if exists some user with cpf or email
    user.password = pwd_context.hash(user.password)
    user_model = UserModel(**user.__dict__)
    try:
        await user_repository.create_user(db, user_model)
        return user_model
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email and cpf must be unique',
        )
