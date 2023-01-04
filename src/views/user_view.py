from datetime import date, datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    cpf: str
    birth_day: date

    class Config:
        orm_mode = True


class UserView(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    birth_day: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
