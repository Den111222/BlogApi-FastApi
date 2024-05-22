from abc import ABC, abstractmethod
from uuid import UUID

from models.schemas.category import Category, CategoryList, CategoryCreate
from models.schemas.post import Post, PostCreate
from models.schemas.tag import Tag, TagList
from db.storage.postgre.postgre_session import get_session


class AbstractPostRepository(ABC):
    @abstractmethod
    async def if_exist(self, title: str, author_login: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_post_by_id(self, id: UUID) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    async def get_post_by_title_author(self, title, author_login) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    async def get_posts_by_author(
        self, author_login: str, page: int, page_size: int
    ) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    async def create_post(self, _post: PostCreate) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def update_post(self, post_id: UUID, update_data: dict) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def delete_post(self, author_login: str, post_id: UUID) -> Post:
        raise NotImplementedError


class AbstractCategoryRepository(ABC):
    @abstractmethod
    async def get_category_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def get_category_by_name(self, name: str) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def get_categories(self, page: int, page_size: int) -> CategoryList | None:
        raise NotImplementedError

    @abstractmethod
    async def create_category(self, _category: CategoryCreate) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def update_category(self, category_id: UUID, update_data: dict) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def delete_category(self, category_id: UUID) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def if_exist(self, title: str) -> bool:
        raise NotImplementedError


class AbstractTagRepository(ABC):
    @abstractmethod
    async def get_tags(self, page: int, page_size: int) -> TagList | None:
        raise NotImplementedError

    @abstractmethod
    async def create_tag(self, _tag: Tag) -> Tag:
        raise NotImplementedError

    @abstractmethod
    async def update_tag(self, tag_id: UUID, update_data: dict) -> Tag:
        raise NotImplementedError

    @abstractmethod
    async def delete_tag(self, category_id: UUID) -> Tag:
        raise NotImplementedError

    @abstractmethod
    async def if_exist(self, name: str) -> bool:
        raise NotImplementedError
