from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.sql import func

from utils.database import Base


class AnuncioModel(Base):
    __tablename__ = 'anuncio'

    pet_id = Column(Integer, ForeignKey('pet.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('base_users.id'), primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(350), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())
