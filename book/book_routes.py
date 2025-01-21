import logging

from fastapi import APIRouter, Query

from deps import SessionDep, CurrentUserDep
from schemas import SBookCreate, SBook, SBookUpdate, SBookShort
from user.role_checker import AdminOnlyAccess
from .book_service import BookService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/book",
    tags=["Управление книгами"],
)


@router.post("/", dependencies=[AdminOnlyAccess])
async def create_book(
        book_create: SBookCreate,
        session: SessionDep
) -> SBook:
    return await BookService.create_book(session, book_create)


@router.patch("/{book_id}", dependencies=[AdminOnlyAccess])
async def update_book(
        book_id: int,
        book_update: SBookUpdate,
        session: SessionDep
) -> SBook:
    return await BookService.update_book(session, book_id, book_update)


@router.get("/{book_id}")
async def get_book(
        book_id: int,
        session: SessionDep,
        _: CurrentUserDep
) -> SBook:
    return await BookService.get_book_by_id(session, book_id)


@router.delete("/{book_id}", dependencies=[AdminOnlyAccess])
async def delete_book(
        book_id: int,
        session: SessionDep
):
    return await BookService.delete_book(session, book_id)


@router.get("/")
async def get_all_books(
        session: SessionDep,
        _: CurrentUserDep,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
) -> list[SBookShort]:
    return await BookService.get_all_books(session, limit, offset)
