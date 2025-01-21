import logging
from datetime import date, timedelta

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import BookNotFoundException, BookNotAvailableException, LimitBorrowingException, \
    BorrowingNotFoundException
from models import User, Book, Borrowing

logger = logging.getLogger(__name__)


class BorrowingService:

    MAX_BORROWED_BOOKS = 5
    COUNT_BORROWING_DAYS = 14

    @classmethod
    async def borrow_book(cls, session: AsyncSession, user: User, book_id: int, count_days: int = COUNT_BORROWING_DAYS) -> Borrowing:
        book = await session.get(Book, book_id)
        if not book:
            raise BookNotFoundException
        if book.available_copies <= 0:
            raise BookNotAvailableException

        count_borrowing = (
            await session.execute(
                select(func.count("*")).where(and_(Borrowing.user_id == user.id, Borrowing.is_returned == False))
            )
        ).scalar()
        if count_borrowing >= cls.MAX_BORROWED_BOOKS:
            raise LimitBorrowingException

        book.available_copies -= 1

        borrowing = Borrowing(
            user_id=user.id,
            book_id=book_id,
            borrow_date=date.today(),
            return_date=date.today() + timedelta(days=count_days)
        )
        session.add(borrowing)
        await session.commit()
        await session.refresh(borrowing)
        return borrowing


    @classmethod
    async def return_book(cls, session: AsyncSession, user: User, book_id: int) -> Borrowing:
        borrowing = (
            await session.execute(
                select(Borrowing).where(and_(Borrowing.user_id == user.id, Borrowing.book_id == book_id, Borrowing.is_returned == False))
            )
        ).scalar()
        if not borrowing:
            raise BorrowingNotFoundException

        borrowing.is_returned = True
        borrowing.book.available_copies += 1
        await session.commit()
        await session.refresh(borrowing)
        return borrowing


    @classmethod
    async def get_all_borrowing_for_user(cls, session: AsyncSession, user: User):
        return await session.scalars(
            select(Borrowing).where(and_(Borrowing.user_id == user.id, Borrowing.is_returned == False))
        )