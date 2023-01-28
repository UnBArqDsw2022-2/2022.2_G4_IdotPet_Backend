from datetime import datetime
from typing import Literal

from pydantic import BaseModel, validator
from models.pet_model import PetStatus

from utils.optional_fields_metaclass import AllOptionalMeta
from utils.settings import settings
from utils import base64


class PetCreate(BaseModel):
    name: str
    description: str = ''
    age: int
    specie_name: str
    breed_name: str
    image: str | None = None
    size: str
    gender: Literal['f', 'm']
    vaccine: bool

    @validator('image')
    def validate_image(cls, value: str | bytes):
        if value is None:
            return None

        if base64.is_base64(value):
            return base64.decode(value)

        raise ValueError('Formato inválido para imagem')

    class Config:
        orm_mode = True


class PetUpdate(PetCreate, metaclass=AllOptionalMeta):
    ...


class PetView(BaseModel):
    id: int
    name: str
    description: str
    age: int
    specie_name: str
    breed_name: str
    image: str | None
    size: str
    gender: Literal['F', 'M']
    vaccine: bool
    status: PetStatus
    created_at: datetime
    updated_at: datetime

    @validator('image', pre=True)
    def must_be_url(cls, value, values):
        if not isinstance(value, bytes):
            return None

        return f'{settings.BASE_API_URL}/pet/image/{values["id"]}'

    class Config:
        orm_mode = True
        validate_assignment = True
