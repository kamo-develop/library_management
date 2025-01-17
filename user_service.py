from sqlalchemy import select

from database import async_session_maker
from models import User


class UserService:

    @classmethod
    async def get_all_users(cls):
        """Возвращает всех пользователей"""
        async with async_session_maker() as session:
            users = await session.execute(select(User))
            return users.scalars().all()

    @classmethod
    async def get_user_by_username(cls, username):
        """Ищет пользователя по логину"""
        async with async_session_maker() as session:
            user = await session.execute(select(User).filter(User.username == username))
            return user.first()

