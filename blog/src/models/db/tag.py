from sqlalchemy import Column, String, Uuid
from models.db.post import post_tag_association_table

from sqlalchemy.orm import relationship

from models.db import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Uuid, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    posts = relationship(
        "Post",
        secondary=post_tag_association_table,
        back_populates="tags",
        cascade="all, delete",
    )
