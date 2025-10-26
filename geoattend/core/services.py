from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..db import crud
from .. import schemas


async def register_new_user(
    db: AsyncSession, user_in: schemas.UserCreate
) -> schemas.UserRead:
    # Check if user already exists
    db_user = await crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = await crud.create_user(db, user=user_in)

    return schemas.UserRead.from_orm(new_user)
