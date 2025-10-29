import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from geoattend.db.models import Base
from geoattend.main import app
from geoattend.api.v1.router_users import get_db

# --- Database Setup ---
# We use an in memory SQLite database for isolated tests
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# explaining url composition:
"""
sqlite: The database dialect. 
It's not main PostgreSQL server; it's a simple, serverless, file-based database.

+aiosqlite: The driver. 
This is the crucial part. It's an asynchronous driver. 
This allows pytest (using the pytest-asyncio plugin) to run async def test functions and await database calls, just like the real app.

:///:memory:: The location. 
This is a special "filename" for SQLite. It tells SQLite: "Don't create a database file on the hard drive. 
Create the entire database purely in RAM (the computer's memory) 🧠."
"""

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# create table for every test (fixture)
@pytest.fixture(scope="function")
async def db_session():
    # Create the tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        # Drop the tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# Override "get_db" dependency
# to use the test database instead of the real one.
@pytest.fixture(scope="function")
def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    # Override the dependency in the app
    app.dependency_overrides[get_db] = _override_get_db
    yield
    # Clear the override after the test
    app.dependency_overrides.clear()


# Fixture HTTP client to make requests to the app
@pytest.fixture(scope="function")
async def test_client(override_get_db):
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
