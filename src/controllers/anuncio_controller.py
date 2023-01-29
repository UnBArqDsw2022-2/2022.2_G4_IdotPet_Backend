from fastapi import APIRouter, Depends, HTTPException, status

from models import AnuncioModel, PetModel
from repositories import repository_factory
from schemes.anuncio_schemes import AnuncioCreate, AnuncioUpdate, AnuncioView
from utils.database import AsyncSession, get_db
from utils.security import decode_token

router = APIRouter(prefix='/anuncio', tags=['Anúncio'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnuncioView)
async def create(anuncio: AnuncioCreate, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    if not await is_pet_from_user(anuncio.pet_id, logger_user_id, db):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Pet não encontrado')

    anuncio_model = AnuncioModel(
        **{**anuncio.dict(exclude_unset=True), 'user_id': logger_user_id}
    )
    repository = await repository_factory(AnuncioModel, db)
    await repository.create(anuncio_model)
    return anuncio_model


async def is_pet_from_user(pet_id: int, user_id: int, db: AsyncSession) -> bool:
    repository = await repository_factory(PetModel, db)
    return bool(await repository.get_all({'id': pet_id, 'user_id': user_id}))


@router.get('/', status_code=status.HTTP_201_CREATED, response_model=AnuncioView, dependencies=[Depends(decode_token)])
async def anuncio_get_all(db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    return await repository.get_all()


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView, dependencies=[Depends(decode_token)])
async def patch(anuncio: AnuncioUpdate, id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio_model = await repository.get_by_id(id)
    for key, value in anuncio.__dict__.items():
        if value is None:
            continue

        setattr(anuncio_model, key, value)

    return await repository.update(anuncio_model)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView, dependencies=[Depends(decode_token)])
async def update(anuncio: AnuncioUpdate, id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio_model = await repository.get_by_id(id)
    for key, value in anuncio.__dict__.items():
        setattr(anuncio_model, key, value)

    return await repository.update(anuncio_model)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView, dependencies=[Depends(decode_token)])
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio = await repository.get_by_id(id)
    return await repository.delete(anuncio)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView, dependencies=[Depends(decode_token)])
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    return await repository.get_by_id(id)
