from pydantic import BaseModel

from models import UserRole


class SUserRegister(BaseModel):
    username: str
    fullname: str | None = None
    password: str

class SUser(BaseModel):
    username: str
    fullname: str | None = None
    role: UserRole

    # class Config:
    #     from_attributes = True




