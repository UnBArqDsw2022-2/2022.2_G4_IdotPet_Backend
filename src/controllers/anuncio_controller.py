from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError

from models import AnuncioModel, BaseUserModel
from repositories import repository_factory
from schemes.anuncio_schemes import AnuncioCreate, AnuncioUpdate, AnuncioView
from utils.database import AsyncSession, get_db
from utils.security import logged_user

router = APIRouter(prefix='/anuncio', tags=['Anúncio'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnuncioView)
async def create(anuncio: AnuncioCreate, current_user: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    try:
        anuncio_model = AnuncioModel(**{**anuncio.dict(exclude_unset=True), 'user_id': current_user.id})
        repository = await repository_factory(AnuncioModel, db)
        await repository.create(anuncio_model)
        return anuncio_model
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email and cpf must be unique',
        )

@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView)
async def patch(anuncio: AnuncioUpdate, id: int, _: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio_model = await repository.get_by_id(id)
    for key, value in anuncio.__dict__.items():
        if value is None:
            continue

        setattr(anuncio_model, key, value)

    return await repository.update(anuncio_model)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView)
async def update(anuncio: AnuncioUpdate, id: int, _: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio_model = await repository.get_by_id(id)
    for key, value in anuncio.__dict__.items():
        setattr(anuncio_model, key, value)

    return await repository.update(anuncio_model)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView)
async def delete(id: int, _: BaseUserModel = Depends(logged_user), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    anuncio = await repository.get_by_id(id)
    return await repository.delete(anuncio)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AnuncioView, dependencies=[Depends(logged_user)])
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    return await repository.get_by_id(id)

@router.get('/', status_code=status.HTTP_201_CREATED, response_model=AnuncioView)
async def anuncio_get_all(db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(AnuncioModel, db)
    return await repository.get_all()
