from pydantic import BaseModel, Field, conlist
from datetime import date
from models import UserRole


class SUserRegister(BaseModel):
    username: str = Field(max_length=30)
    fullname: str | None = None
    password: str


class SUser(BaseModel):
    id: int
    username: str
    fullname: str | None = None
    role: UserRole


class SUserUpdate(BaseModel):
    fullname: str | None = None


class SToken(BaseModel):
    access_token: str
    token_type: str


class SAuthorCreate(BaseModel):
    name: str = Field(max_length=50)
    biography: str | None = None
    birth_date: date


class SAuthorUpdate(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    biography: str | None = None
    birth_date: date | None = None


class SAuthor(BaseModel):
    id: int
    name: str = Field(max_length=50)
    biography: str | None = None
    birth_date: date


class SBookCreate(BaseModel):
    title: str
    description: str | None = None
    publication_date: date
    genres: str
    available_copies: int = Field(ge=0, default=0)
    authors: conlist(int, min_length=1)


class SBookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    publication_date: date | None = None
    genres: str | None = None
    available_copies: int | None = Field(ge=0, default=None)
    authors: conlist(int) | None = None


class SBook(BaseModel):
    id: int
    title: str
    description: str | None = None
    publication_date: date
    genres: str
    available_copies: int = Field(ge=0, default=0)
    authors: conlist(SAuthor, min_length=1)


class SBookShort(BaseModel):
    id: int
    title: str
    available_copies: int = Field(ge=0, default=0)


class SBorrowing(BaseModel):
    borrow_date: date
    return_date: date
    is_returned: bool
    book: SBookShort