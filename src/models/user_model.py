from sqlalchemy import Column, String, Integer, ForeignKey

from .base_user_model import BaseUserModel


class UserModel(BaseUserModel):
    __tablename__ = 'users'

    id = Column(Integer, ForeignKey('base_users.id'), primary_key=True)
    cpf = Column(String(11), unique=True, nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'user'}
