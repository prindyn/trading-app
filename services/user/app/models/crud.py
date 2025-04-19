from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.tables import User
from app.core.auth import hash_password


async def create_user(db: AsyncSession, user):
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user_id: int, new_email: str):
    await db.execute(update(User).where(User.id == user_id).values(email=new_email))
    await db.commit()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter_by(email=email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter_by(id=user_id))
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user_password(db: AsyncSession, user_id: int, new_password: str):
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(hashed_password=hash_password(new_password))
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()


async def delete_user(db: AsyncSession, user_id: int):
    stmt = delete(User).where(User.id == user_id)
    await db.execute(stmt)
    await db.commit()
