from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from repositories import UserRepository
from utils.security import decode_token, generate_token, pwd_context
from views.user_view import UserCreate, UserView

router = APIRouter(prefix='/user', tags=['Usuário'])


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repository: UserRepository = Depends(UserRepository)):
    user = await repository.get_user_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {'access_token': generate_token(user.id), 'token_type': 'bearer'}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserView)
async def create(user: UserCreate, repository: UserRepository = Depends(UserRepository)):
    # TODO: Validate email and cpf
    #   Check if exists some user with cpf or email
    user_model = UserModel(**user.dict())
    try:
        await repository.create(user_model)
        return user_model
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email and cpf must be unique',
        )


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserView, dependencies=[Depends(decode_token)])
async def get_by_id(id: int, repository: UserRepository = Depends(UserRepository)):
    user = await repository.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user
