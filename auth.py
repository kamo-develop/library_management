from typing import Annotated

from fastapi import APIRouter, HTTPException

from schemas import SUserRegister, SUser
from user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],  #tags
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
async def register_user(user_register: SUserRegister):
    db_user = await UserService.get_user_by_username(user_register.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    pass

@router.get("/users")
async def get_all_users() -> list[SUser]:
    return await UserService.get_all_users()
