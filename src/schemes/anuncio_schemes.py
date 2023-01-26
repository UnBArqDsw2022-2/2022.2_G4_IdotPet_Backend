import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, validator

from utils.optional_fields_metaclass import AllOptionalMeta
from utils.settings import settings
from utils import base64


class AnuncioCreate(BaseModel):
    # Base fields
    id_pet = int
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AnuncioUpdate(AnuncioCreate, metaclass=AllOptionalMeta):
    ...
