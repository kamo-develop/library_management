from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
import logging
from jose import JWTError, jwt
from config import settings
from database import async_session_maker
from models import User
from schemas import SUserRegister
from .security import get_password_hash, verify_password, oauth2_scheme

logger = logging.getLogger(__name__)


class UserService:

    @classmethod
    async def get_all_users(cls) -> list[User]:
        """Возвращает всех пользователей"""
        async with async_session_maker() as session:
            users = await session.execute(select(User))
            return users.scalars().all()

    @classmethod
    async def get_user_by_username(cls, username) -> User:
        """Ищет пользователя по логину"""
        async with async_session_maker() as session:
            user = await session.execute(select(User).filter(User.username == username))
            return user.scalars().first()

    @classmethod
    async def get_user_by_id(cls, user_id) -> User:
        """Ищет пользователя по логину"""
        async with async_session_maker() as session:
            user = await session.execute(select(User).filter(User.id == user_id))
            return user.scalars().first()

    @classmethod
    async def create_user(cls, user_register: SUserRegister):
        hashed_password = get_password_hash(user_register.password)
        new_user = User(username=user_register.username, fullname=user_register.fullname, password=hashed_password)
        async with async_session_maker() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    @classmethod
    async def authenticate_user(cls, username, password) -> User | None:
        user = await cls.get_user_by_username(username=username)
        logger.info(user)
        if not user or not verify_password(password, user.password):
            return None
        return user

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("id")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await cls.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user

