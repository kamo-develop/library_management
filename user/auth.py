from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm
from models import UserRole, User
from schemas import SUserRegister, SUser, SToken
from .role_checker import RoleChecker
from .security import create_access_token
from .user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Управление пользователями и аутентификация"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register_user(user_register: SUserRegister) -> SUser:
    existing_user = await UserService.get_user_by_username(user_register.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    new_user = await UserService.create_user(user_register)
    return new_user


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SToken:
    user = await UserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"id": user.id, "username": user.username})
    return SToken(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def get_user_me(current_user: Annotated[User, Depends(UserService.get_current_user)]) -> SUser:
    return current_user


@router.get("/users", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def get_all_users() -> list[SUser]:
    return await UserService.get_all_users()
