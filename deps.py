from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from config import settings
from database import get_db
from exceptions import UserNotFoundException, InvalidTokenException, UnknownTokenException
from models import User
from user.security import oauth2_scheme

SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
        session: SessionDep,
        token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise UnknownTokenException
    except JWTError:
        raise InvalidTokenException
    user = await session.get(User, user_id)
    if user is None:
        raise UserNotFoundException
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]

