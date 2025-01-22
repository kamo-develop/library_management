import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from exceptions import UserNotFoundException
from models import User, UserRole
from schemas import SUserRegister, SUserUpdate
from utils import copy_model_attributes
from .security import get_password_hash, verify_password

logger = logging.getLogger(__name__)


class UserService:
    @classmethod
    async def get_all_users(cls, session: AsyncSession, limit: int, offset: int):
        # Поиск всех пользователей
        return await session.scalars(select(User).limit(limit).offset(offset))

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username) -> User:
        # Поиск пользователя по имени
        return await session.scalar(select(User).filter(User.username == username))

    @classmethod
    async def create_user(cls, session: AsyncSession, user_register: SUserRegister) -> User:
        hashed_password = get_password_hash(user_register.password)
        new_user = User(username=user_register.username, fullname=user_register.fullname, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        logger.info(f"Created new user: {new_user}")
        return new_user

    @classmethod
    async def update_user(cls, session: AsyncSession, user: User, user_update: SUserUpdate) -> User:
        user_dict = user_update.model_dump(exclude_unset=True)
        copy_model_attributes(data=user_dict, model_to=user)
        await session.commit()
        await session.refresh(user)
        logger.info(f"Updated user: {user}")
        return user

    @classmethod
    async def delete_user_by_id(cls, session: AsyncSession, user_id: int):
        user = await session.get(User, user_id)
        if not user:
            raise UserNotFoundException
        await session.delete(user)
        await session.commit()
        logger.info(f"Deleted user with id={user_id}")

    @classmethod
    async def authenticate_user(cls, session: AsyncSession, username, password) -> User | None:
        user = await cls.get_user_by_username(session, username)
        if not user or not verify_password(password, user.password):
            return None
        logger.info(f"Authenticate user: {user}")
        return user


