from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from models import BaseUserModel, OngUserModel, UserModel
from repositories import BaseUserRepository, repository_factory
from schemes.user_schemes import UserCreate, UserUpdate, AnyUserView
from utils.database import AsyncSession, get_db
from utils.security import generate_token, logged_user

router = APIRouter(prefix='/user', tags=['Usuário'])


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    repository = BaseUserRepository(BaseUserModel, db)
    user_id = await repository.verify_user_password(form_data.username, form_data.password)
    return {'access_token': generate_token(user_id), 'token_type': 'bearer'}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnyUserView)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Validate email and cpf
    #   Check if exists some user with cpf or email
    try:
        user_model_class = deduce_user_model_class(user)
        user_model = user_model_class(**user.dict(exclude_unset=True))
        repository = await repository_factory(user_model_class, db)
        await repository.create(user_model)
        return user_model
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email and cpf must be unique',
        )


def deduce_user_model_class(user: UserCreate) -> type[BaseUserModel]:
    if user.user_type == UserModel.__mapper_args__['polymorphic_identity']:
        return UserModel
    if user.user_type == OngUserModel.__mapper_args__['polymorphic_identity']:
        return OngUserModel
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid user_type')


@router.get('/logged', status_code=status.HTTP_200_OK, response_model=AnyUserView)
async def get_logged_user(current_user: BaseUserModel = Depends(logged_user)):
    return current_user


@router.patch('/', status_code=status.HTTP_200_OK, response_model=AnyUserView)
async def patch(user: UserUpdate, current_user: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(BaseUserModel, db)
    for key, value in user.__dict__.items():
        if value is None:
            continue

        setattr(current_user, key, value)

    return await repository.update(current_user)


@router.put('/', status_code=status.HTTP_200_OK, response_model=AnyUserView)
async def update(user: UserCreate, current_user: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(BaseUserModel, db)
    for key, value in user.__dict__.items():
        setattr(current_user, key, value)

    return await repository.update(current_user)


@router.delete('/', status_code=status.HTTP_200_OK, response_model=AnyUserView)
async def delete(current_user: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(BaseUserModel, db)
    return await repository.delete(current_user)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AnyUserView, dependencies=[Depends(logged_user)])
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(BaseUserModel, db)
    return await repository.get_by_id(id)


@router.get('/image/{id}', status_code=status.HTTP_200_OK, dependencies=[])
async def read_image(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(BaseUserModel, db)
    user = await repository.get_by_id(id)
    if not user.image:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Usuário não possui imagem')

    return Response(content=user.image, media_type='image/png')
