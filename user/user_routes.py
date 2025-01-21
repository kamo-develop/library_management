from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends, Query
import logging
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from deps import CurrentUserDep, SessionDep
from models import UserRole, User
from schemas import SUserRegister, SUser, SToken, SUserUpdate
from .role_checker import AdminOnlyAccess
from .security import create_access_token
from .user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["Управление пользователями и аутентификация"],
)


@router.post("/register")
async def register_user(
        user_register: SUserRegister,
        session: SessionDep
) -> SUser:
    existing_user = await UserService.get_user_by_username(session, user_register.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    return await UserService.create_user(session, user_register)


@router.post("/login")
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep
) -> SToken:
    user = await UserService.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"id": user.id, "username": user.username})
    return SToken(access_token=access_token, token_type="bearer")


@router.patch("/me")
async def update_user(
        user_update: SUserUpdate,
        current_user: CurrentUserDep,
        session: SessionDep,
) -> SUser:
    return await UserService.update_user(session, current_user, user_update)


@router.get("/me")
async def get_user_me(
        current_user: CurrentUserDep
) -> SUser:
    return current_user


@router.get("/all", dependencies=[AdminOnlyAccess])
async def get_all_users(
        session: SessionDep,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
) -> list[SUser]:
    return await UserService.get_all_users(session, limit, offset)


@router.delete("/{user_id}", dependencies=[AdminOnlyAccess])
async def delete_user(
        user_id: int,
        session: SessionDep
):
    await UserService.delete_user_by_id(session, user_id)
