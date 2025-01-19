from typing import Optional, List
import enum
from sqlalchemy import String, Enum, Date, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import date

from database import Base


class UserRole(enum.Enum):
    READER = "reader"
    ADMIN = "admin"


UserRoleType: Enum = Enum(
    UserRole,
    name="user_role_type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    password: Mapped[str]
    role: Mapped[UserRoleType] = mapped_column(UserRoleType, default=UserRole.READER)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.fullname!r}, role={self.role!r})"


book_author_association = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    publication_date: Mapped[date] = mapped_column(Date)
    genres: Mapped[str]
    available_copies: Mapped[int] = mapped_column(default=0)

    authors: Mapped[List["Author"]] = relationship(
        secondary=book_author_association,
        back_populates="books",
        lazy="selectin",
        # cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r}, birth_date={self.birth_date!r},)"


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[Optional[str]]
    birth_date: Mapped[date] = mapped_column(Date)

    books: Mapped[List[Book]] = relationship(secondary=book_author_association, back_populates="authors")

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r}, birth_date={self.birth_date!r},)"





