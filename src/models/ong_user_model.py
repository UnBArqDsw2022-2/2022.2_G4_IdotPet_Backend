from sqlalchemy import Column, String, Integer, ForeignKey

from .base_user_model import BaseUserModel


class OngUserModel(BaseUserModel):
    __tablename__ = 'ong_users'

    id = Column(Integer, ForeignKey('base_users.id'), primary_key=True)
    cnpj = Column(String(14), unique=True, nullable=False)
    pix = Column(String(512))

    __mapper_args__ = {'polymorphic_identity': 'ong'}
