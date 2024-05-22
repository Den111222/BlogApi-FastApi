import asyncio
import logging
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import app_settings_test
from db.storage import get_session

from main import app
from models.db import Base, Role, role_user
from tests.functional.testdata.roles_data import get_role_data, get_role_user_data
from tests.functional.testdata.users_data import get_user_data


LOGGER = logging.getLogger(__name__)

# DATABASE
DATABASE_URL_TEST = app_settings_test.database_dsn

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    echo=True,
)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = get_async_session


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with async_session_maker() as session:
        for item in get_user_data():
            session.add(item)
        for item in get_role_data():
            stmt = insert(Role).values(name=item.name)
            await session.execute(stmt)
        for item in get_role_user_data():
            stmt = insert(role_user).values(**item)
            await session.execute(stmt)
        await session.commit()

    yield


app_url = f"http://{app_settings_test.host}:{app_settings_test.port}"


@pytest_asyncio.fixture(scope="session", params=[{"app": app, "base_url": app_url}])
async def ac(request):
    async with AsyncClient(**request.param) as ac:
        yield ac
