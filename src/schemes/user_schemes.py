import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, validator

from utils.optional_fields_metaclass import AllOptionalMeta
from utils.settings import settings
from utils import base64


class UserCreate(BaseModel):
    # Base fields
    name: str
    user_type: Literal['user', 'ong']
    image: bytes | None = None
    name: str
    email: EmailStr
    password: str
    birth_day: date
    # User fields
    cpf: str | None
    # Ong fields
    cnpj: str | None
    pix: str | None

    @validator('image')
    def validate_image(cls, value: str | bytes):
        if value is None:
            return None

        if base64.is_base64(value):
            return base64.decode(value)

        raise ValueError('Formato inválido para imagem')

    @validator('cpf')
    def validate_cpf(cls, value: str, values):
        if values['user_type'] != 'user':
            return None

        value = re.sub(r'\D', '', value)  # remove mask if present
        if not re.fullmatch(r'\d{11}', value):
            raise ValueError('Formato inválido para CPF')
        return value

    @validator('cnpj')
    def validate_cnpj(cls, value: str, values):
        if values['user_type'] != 'ong':
            return None

        value = re.sub(r'\D', '', value)  # remove mask if present
        if not re.fullmatch(r'\d{14}', value):
            raise ValueError('Formato inválido para CNPJ')
        return value

    class Config:
        orm_mode = True


class UserUpdate(UserCreate, metaclass=AllOptionalMeta):
    ...


class BaseUserView(BaseModel):
    id: int
    user_type: Literal['user', 'ong']
    image: str | None
    name: str
    birth_day: date
    created_at: datetime
    updated_at: datetime

    @validator('image', pre=True)
    def must_be_url(cls, value, values):
        if not isinstance(value, bytes):
            return None

        return f'{settings.BASE_API_URL}/user/image/{values["id"]}'

    class Config:
        orm_mode = True
        validate_assignment = True


class UserView(BaseUserView):
    cpf: str


class OngUserView(BaseUserView):
    cnpj: str
    pix: str | None


AnyUserView = OngUserView | UserView
