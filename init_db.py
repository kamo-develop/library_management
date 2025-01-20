import asyncio
from config import settings
from database import async_session
from models import User, UserRole
from schemas import SUserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from user.user_service import UserService


async def create_admin(session: AsyncSession):
    user = (
        await session.execute(select(User).where(User.username == settings.FIRST_SUPERUSER))
    ).first()
    if not user:
        user_register = SUserRegister(
            username=settings.FIRST_SUPERUSER,
            fullname=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD
        )
        new_user = await UserService.create_user(session, user_register)
        new_user.role = UserRole.ADMIN
        await session.commit()


async def init_db():
    async with async_session() as session:
        await create_admin(session)


asyncio.run(init_db())