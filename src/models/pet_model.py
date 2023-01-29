import enum

from sqlalchemy import (Column, DateTime, Integer, ForeignKey,
                        LargeBinary, String, Enum, ForeignKeyConstraint)
from sqlalchemy.sql import func

from utils.database import Base


class PetStatus(enum.Enum):
    ADOPTED = 1
    ANNOUNCED = 2
    AVAILABLE = 3


class PetBreed(Base):
    __tablename__ = 'pet_breed'

    specie_name = Column(String(150), primary_key=True)
    breed_name = Column(String(150), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), nullable=True)


class PetModel(Base):
    __tablename__ = 'pet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('base_users.id'))
    name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    cep = Column(String(20), nullable=True)
    specie_name = Column(String(150), nullable=False)
    breed_name = Column(String(150), nullable=False)
    image = Column(LargeBinary, nullable=True)
    size = Column(String(150), nullable=False)
    gender = Column(Enum('f', 'm', name='pet_gender'), nullable=False)
    status = Column(Enum(PetStatus), nullable=False, default=PetStatus.AVAILABLE)
    vaccine = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint([specie_name, breed_name],
                             [PetBreed.specie_name, PetBreed.breed_name]),
    )
