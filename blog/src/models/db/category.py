from sqlalchemy import Column, String, Uuid, Boolean

from sqlalchemy.orm import relationship

from models.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Uuid, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    text = Column(String)
    deleted = Column(Boolean, default=False)
    posts = relationship(
        "Post", back_populates="category", cascade="all, delete-orphan"
    )
