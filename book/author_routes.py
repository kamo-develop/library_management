from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from deps import SessionDep, CurrentUserDep
from models import UserRole
from schemas import SAuthorCreate, SAuthor, SAuthorUpdate
from user.role_checker import AdminOnlyAccess
from .author_service import AuthorService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/author",
    tags=["Управление авторами"],
)


@router.post("/", dependencies=[AdminOnlyAccess])
async def create_author(
        author_create: SAuthorCreate,
        session: SessionDep
) -> SAuthor:
    return await AuthorService.create_author(session, author_create)


@router.patch("/{author_id}", dependencies=[AdminOnlyAccess])
async def update_author(
        author_id: int,
        author_create: SAuthorUpdate,
        session: SessionDep
) -> SAuthor:
    return await AuthorService.update_author(session, author_id, author_create)


@router.get("/{author_id}")
async def get_author(
        author_id: int,
        session: SessionDep,
        _: CurrentUserDep
) -> SAuthor:
    return await AuthorService.get_author_by_id(session, author_id)


@router.delete("/{author_id}", dependencies=[AdminOnlyAccess])
async def delete_author(
        author_id: int,
        session: SessionDep
):
    return await AuthorService.delete_author(session, author_id)