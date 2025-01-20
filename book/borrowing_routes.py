from fastapi import APIRouter

from book.borrowing_service import BorrowingService
from deps import SessionDep, CurrentUserDep
from schemas import SBorrowing

router = APIRouter(
    prefix="/borrowing",
    tags=["Взятие и возврат книг"],
)


@router.post("/{book_id}")
async def borrowing_book(
        book_id: int,
        session: SessionDep,
        current_user: CurrentUserDep
) -> SBorrowing:
    return await BorrowingService.borrow_book(session, current_user, book_id)


@router.post("/return/{book_id}")
async def return_book(
        book_id: int,
        session: SessionDep,
        current_user: CurrentUserDep
) -> SBorrowing:
    return await BorrowingService.return_book(session, current_user, book_id)


@router.get("/all")
async def get_all_borrowing_book(
        session: SessionDep,
        current_user: CurrentUserDep
) -> list[SBorrowing]:
    return await BorrowingService.get_all_borrowing_for_user(session, current_user)