import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession


pytestmark = pytest.mark.asyncio


async def test_create_user(test_client: AsyncClient, db_session: AsyncSession):
    # --- Arrange ---
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
    }

    # --- Act ---
    response = await test_client.post("/api/v1/users/", json=user_data)

    # --- Assert ---
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # Make sure password isn't returned
