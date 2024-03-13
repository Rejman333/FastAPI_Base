from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDAsyncBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.core.utils import hash_password, verify_password


class CRUDUser(CRUDAsyncBase[User, UserCreate, UserUpdate, UserResponse, List[UserResponse]]):
    async def get_by_email(self, db_session: AsyncSession, *, email: str) -> User | None:
        return (await db_session.scalars(select(User).where(User.email == email))).first()

    # ToDo Recreate
    async def create(self, db_session: AsyncSession, *, create_schema: UserCreate) -> User:
        user_model = User(**create_schema.dict())
        db_session.add(user_model)
        await db_session.commit()
        await db_session.refresh(user_model)
        return user_model


async def authenticate(self, db_session: AsyncSession, *, login_schema: UserLogin) -> User | None:
    user = await self.get_by_email(db_session, email=login_schema.email)
    if not user:
        return None
    if not verify_password(login_schema.password.get_secret_value(), user.hashed_password):
        return None
    return user
