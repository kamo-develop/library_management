from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import logging
from jose import JWTError, jwt
from config import settings
from models import User
from schemas import SUserRegister, SUserUpdate
from utils import copy_model_attributes
from .security import get_password_hash, verify_password

logger = logging.getLogger(__name__)


class UserService:
    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> list[User]:
        """Возвращает всех пользователей"""
        return (await session.execute(select(User))).scalars().all()

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username) -> User:
        """Ищет пользователя по логину"""
        return (await session.execute(select(User).filter(User.username == username))).scalars().first()

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id) -> User:
        """Ищет пользователя по логину"""
        return (await session.execute(select(User).filter(User.id == user_id))).scalars().first()

    @classmethod
    async def create_user(cls, session: AsyncSession, user_register: SUserRegister) -> User:
        hashed_password = get_password_hash(user_register.password)
        new_user = User(username=user_register.username, fullname=user_register.fullname, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def update_user(cls, session: AsyncSession, user: User, user_update: SUserUpdate) -> User:
        user_dict = user_update.model_dump(exclude_unset=True)
        copy_model_attributes(data=user_dict, model_to=user)
        await session.commit()
        await session.refresh(user)
        return user

    @classmethod
    async def delete_user_by_id(cls, session: AsyncSession, user_id: int):
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()

    @classmethod
    async def authenticate_user(cls, session: AsyncSession, username, password) -> User | None:
        user = await cls.get_user_by_username(session, username)
        if not user or not verify_password(password, user.password):
            return None
        return user

