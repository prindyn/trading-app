from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import UserCreate, UserOut
from app.core.database import get_session
from app.models.crud import (
    get_user_by_email,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)

router = APIRouter()


@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_session)):
    return await get_all_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user_info(
    user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_session)
):
    return await update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(user_id: int, db: AsyncSession = Depends(get_session)):
    await delete_user(db, user_id)
    return
