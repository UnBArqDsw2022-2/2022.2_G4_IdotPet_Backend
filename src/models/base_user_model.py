from sqlalchemy import Column, Date, DateTime, Integer, String, LargeBinary
from sqlalchemy.sql import func

from utils.database import Base


class BaseUserModel(Base):
    __tablename__ = 'base_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_type = Column(String(32), nullable=False)
    image = Column(LargeBinary, nullable=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    birth_day = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())

    __mapper_args__ = {'polymorphic_on': user_type}
