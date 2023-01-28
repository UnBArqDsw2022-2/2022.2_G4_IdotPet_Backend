from datetime import datetime

from pydantic import BaseModel

from utils.optional_fields_metaclass import AllOptionalMeta


class AnuncioCreate(BaseModel):
    # Base fields
    pet_id: int
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class AnuncioUpdate(AnuncioCreate, metaclass=AllOptionalMeta):
    ...

class AnuncioView(BaseModel):
    id: int
    title : str
    user_id : int
    pet_id : int
    # pet_id : Column(Integer, ForeignKey('pet.id'))
    description : str | None
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True
