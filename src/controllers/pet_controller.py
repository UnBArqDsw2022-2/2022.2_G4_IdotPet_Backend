from fastapi import APIRouter, Depends, HTTPException, status, Response

from models import PetModel
from repositories import repository_factory
from schemes.pet_schemes import PetCreate, PetUpdate, PetView
from utils.database import AsyncSession, get_db
from utils.security import decode_token

router = APIRouter(prefix='/pet', tags=['Pet'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PetView)
async def create(pet: PetCreate, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    pet_model = PetModel(**{**pet.dict(exclude_unset=True), 'user_id': logger_user_id})
    repository = await repository_factory(PetModel, db)
    return await repository.create(pet_model)


@router.get('/', status_code=status.HTTP_200_OK, response_model=PetView, dependencies=[Depends(decode_token)])
async def get_all(db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    return await repository.get_all()


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=PetView)
async def patch(pet: PetUpdate, id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    pet_model = await repository.get_by_id(id)
    if pet_model.user_id != logger_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Você não possui permissão para atualizar esse Pet')

    for key, value in pet.__dict__.items():
        if value is None:
            continue

        setattr(pet_model, key, value)

    return await repository.update(pet_model)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PetView)
async def update(pet: PetUpdate, id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    pet_model = await repository.get_by_id(id)
    if pet_model.user_id != logger_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Você não possui permissão para atualizar esse Pet')

    for key, value in pet.__dict__.items():
        setattr(pet_model, key, value)

    return await repository.update(pet_model)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=PetView)
async def delete(id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    to_delete = await repository.get_by_id(id)
    if to_delete.user_id != logger_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Você não possui permissão para atualizar esse Pet')

    return await repository.delete(to_delete)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PetView, dependencies=[Depends(decode_token)])
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    return await repository.get_by_id(id)


@router.get('/image/{id}', status_code=status.HTTP_200_OK)
async def read_image(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    pet = await repository.get_by_id(id)
    if not pet.image:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Usuário não possui imagem')

    return Response(content=pet.image, media_type='image/png')
