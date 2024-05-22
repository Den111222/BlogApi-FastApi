from sqlalchemy import Column, String, DateTime, Boolean, Uuid
from datetime import datetime

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True)
    login = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
