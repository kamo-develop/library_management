from typing import Optional
import enum
from sqlalchemy import String, Enum, Column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

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
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.fullname!r}), role={self.role!r}"

