from fastapi import APIRouter, Depends, HTTPException, status, Response

from models import PetModel, PetBreed
from repositories import repository_factory
from schemes.pet_schemes import PetCreate, PetUpdate, PetView, PetBreedCreate
from utils.database import AsyncSession, get_db
from utils.security import decode_token

router = APIRouter(prefix='/pet', tags=['Pet'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PetView)
async def pet_create(pet: PetCreate, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    pet_model = PetModel(**{**pet.dict(exclude_unset=True), 'user_id': logger_user_id})
    repository = await repository_factory(PetModel, db)
    return await repository.create(pet_model)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PetView], dependencies=[Depends(decode_token)])
async def pet_get_all(db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    return await repository.get_all()


@router.get('/logged', status_code=status.HTTP_200_OK, response_model=list[PetView])
async def pet_get_all_logger_user(logged_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    return await repository.get_all({'user_id': logged_user_id})


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=PetView)
async def pet_patch(pet: PetUpdate, id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
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
async def pet_update(pet: PetUpdate, id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    pet_model = await repository.get_by_id(id)
    if pet_model.user_id != logger_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Você não possui permissão para atualizar esse Pet')

    for key, value in pet.__dict__.items():
        setattr(pet_model, key, value)

    return await repository.update(pet_model)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=PetView)
async def pet_delete(id: int, logger_user_id: int = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    to_delete = await repository.get_by_id(id)
    if to_delete.user_id != logger_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Você não possui permissão para atualizar esse Pet')

    return await repository.delete(to_delete)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PetView, dependencies=[Depends(decode_token)])
async def pet_get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    return await repository.get_by_id(id)


@router.get('/image/{id}', status_code=status.HTTP_200_OK)
async def pet_read_image(id: int, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetModel, db)
    pet = await repository.get_by_id(id)
    if not pet.image:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Usuário não possui imagem')

    return Response(content=pet.image, media_type='image/png')


@router.get('/breed/', status_code=status.HTTP_200_OK, response_model=list[PetBreedCreate], dependencies=[Depends(decode_token)], tags=['Breed'])
async def breed_get_all(db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetBreed, db)
    breeds = await repository.get_all()
    return convert_breeds_into_response(breeds)


def convert_breeds_into_response(breeds: list[PetBreed]) -> list[PetBreedCreate]:
    result = {}
    for breed in breeds:
        if breed.specie_name not in result:
            result[breed.specie_name] = []

        result[breed.specie_name].append(breed.breed_name)

    return [PetBreedCreate(specie_name=k, breed_names=v)
            for k, v in result.items()]


@router.put('/breed/', status_code=status.HTTP_200_OK, response_model=PetBreedCreate, dependencies=[Depends(decode_token)], tags=['Breed'])
async def breed_update(breed_create: PetBreedCreate, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetBreed, db)
    breeds = await repository.get_all({'specie_name': breed_create.specie_name})
    all_names = {breed.breed_name for breed in breeds}

    to_delete = {breed for breed in breeds if breed.breed_name not in breed_create.breed_names}
    await repository.delete_all(list(to_delete))

    to_create = [
        PetBreed(specie_name=breed_create.specie_name,
                 breed_name=breed_name)
        for breed_name in breed_create.breed_names
        if breed_name not in all_names
    ]

    await repository.create_all(to_create)

    return breed_create


@router.get('/breed/{specie_name}', status_code=status.HTTP_200_OK, response_model=PetBreedCreate, dependencies=[Depends(decode_token)], tags=['Breed'])
async def breed_get_by_id(specie_name: str, db: AsyncSession = Depends(get_db)):
    repository = await repository_factory(PetBreed, db)
    breeds = await repository.get_all({'specie_name': specie_name})
    result = convert_breeds_into_response(breeds)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Espécie não encontrada')
    return result
