"""init

Revision ID: 4a2a2468907a
Revises: 
Create Date: 2024-05-20 18:58:19.112121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a2a2468907a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "posts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("author_login", sa.String(length=200), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("created_ad", sa.DateTime(), nullable=True),
        sa.Column("published_date", sa.DateTime(), nullable=True),
        sa.Column("published", sa.Boolean(), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("category_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "author_login_title_idx", "posts", ["author_login", "title"], unique=True
    )
    op.create_index(
        op.f("ix_posts_author_login"), "posts", ["author_login"], unique=False
    )
    op.create_index(op.f("ix_posts_title"), "posts", ["title"], unique=False)
    op.create_table(
        "post_tag_association",
        sa.Column("post_id", sa.Uuid(), nullable=True),
        sa.Column("tag_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("post_tag_association")
    op.drop_index(op.f("ix_posts_title"), table_name="posts")
    op.drop_index(op.f("ix_posts_author_login"), table_name="posts")
    op.drop_index("author_login_title_idx", table_name="posts")
    op.drop_table("posts")
    op.drop_table("tags")
    op.drop_table("categories")
    # ### end Alembic commands ###