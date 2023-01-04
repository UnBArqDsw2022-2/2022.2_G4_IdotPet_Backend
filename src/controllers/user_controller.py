from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from repositories import UserRepository
from utils.security import generate_token, logged_user
from views.user_view import UserCreate, UserUpdate, UserView

router = APIRouter(prefix='/user', tags=['Usuário'])


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repository: UserRepository = Depends(UserRepository)):
    user_id = await repository.verify_user_password(form_data.username, form_data.password)
    return {'access_token': generate_token(user_id), 'token_type': 'bearer'}


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


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserView, dependencies=[Depends(logged_user)])
async def get_by_id(id: int, repository: UserRepository = Depends(UserRepository)):
    return await repository.get_by_id(id)


@router.put('/', status_code=status.HTTP_200_OK, response_model=UserView)
async def update(user: UserUpdate = Depends(UserUpdate), current_user: int = Depends(logged_user), repository: UserRepository = Depends(UserRepository)):
    for key, value in user.__dict__.items():
        if value is None:
            continue

        setattr(current_user, key, value)

    return await repository.update(current_user)


@router.delete('/', status_code=status.HTTP_200_OK, response_model=UserView)
async def delete(current_user: int = Depends(logged_user), repository: UserRepository = Depends(UserRepository)):
    return await repository.delete(current_user)
