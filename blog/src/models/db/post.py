from sqlalchemy import Column, String, Boolean, Uuid, DateTime, ForeignKey, Table, Index
from datetime import datetime

from sqlalchemy.orm import relationship

from models.db import Base


# Вспомогательная таблица для связи "многие ко многим" между Post и Tag
post_tag_association_table = Table(
    "post_tag_association",
    Base.metadata,
    Column("post_id", Uuid, ForeignKey("posts.id", ondelete="CASCADE")),
    Column("tag_id", Uuid, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Uuid, primary_key=True)
    author_login = Column(String(200), index=True, nullable=False)
    title = Column(String(200), index=True, nullable=False)
    text = Column(String)
    created_ad = Column(DateTime, default=datetime.utcnow)
    published_ad = Column(DateTime)
    published = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    category_id = Column(
        Uuid, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    category = relationship("Category", back_populates="posts")
    tags = relationship(
        "Tag", secondary=post_tag_association_table, back_populates="posts"
    )

    __table_args__ = (
        Index(
            "author_login_title_idx", "author_login", "title", "deleted", unique=True
        ),
    )
