from sqlalchemy import (Column, Date, DateTime, ForeignKey, Integer, String)
from sqlalchemy.sql import func

from utils.database import Base


class AnuncioModel(Base):
    __tablename__ = 'anuncio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('base_users.id'))
    pet_id = Column(Integer, ForeignKey('pet.id'))
    description = Column(String(350), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())