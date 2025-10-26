from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ... import schemas
from ...db.database import AsyncSessionLocal
from ...core import services

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post(
    "/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED
)
async def create_user_endpoint(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to create a new user.
    """
    try:
        return await services.register_new_user(db=db, user_in=user_in)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
