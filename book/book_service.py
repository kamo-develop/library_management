import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import BookNotFoundException, AuthorNotFoundException
from models import Author, Book
from schemas import SBookCreate, SBookUpdate
from utils import copy_model_attributes

logger = logging.getLogger(__name__)


class BookService:

    @classmethod
    async def create_book(cls, session: AsyncSession, book_create: SBookCreate) -> Book:
        book_dict = book_create.model_dump(exclude_unset=True)
        authors_ids = book_dict['authors']
        book_dict.pop('authors')    # Исключить authors, чтобы корректно создать Book

        new_book = Book(**book_dict)

        # Поиск авторов по списку их id
        authors = (await session.execute(select(Author).where(Author.id.in_(authors_ids)))).scalars().all()
        if not authors:
            logger.info(f"No author has been found for new book {book_create.title}")
            raise AuthorNotFoundException
        new_book.authors = authors

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        logger.info(f"Created new book: {new_book}")
        return new_book

    @classmethod
    async def update_book(cls, session: AsyncSession, book_id: int, book_update: SBookUpdate) -> Book:
        book = await cls.get_book_by_id(session, book_id)
        book_dict = book_update.model_dump(exclude_unset=True)
        if book_update.authors:
            # Поиск авторов по списку их id
            authors_ids = book_dict['authors']
            authors = (await session.execute(select(Author).where(Author.id.in_(authors_ids)))).scalars().all()
            if not authors:
                logger.info(f"No author has been found for new book {book_update.title}")
                raise AuthorNotFoundException
            book.authors = authors

        if 'authors' in book_dict:
            # Исключить authors, чтобы корректно создать Book
            book_dict.pop('authors')
        copy_model_attributes(data=book_dict, model_to=book)

        await session.commit()
        await session.refresh(book)
        logger.info(f"Updated book: {book}")
        return book

    @classmethod
    async def get_book_by_id(cls, session: AsyncSession, book_id: int) -> Book:
        book = await session.get(Book, book_id)
        if not book:
            raise BookNotFoundException
        return book

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id: int):
        book = await cls.get_book_by_id(session, book_id)
        await session.delete(book)
        await session.commit()
        logger.info(f"Deleted book with id={book_id}")


    @classmethod
    async def get_all_books(cls, session: AsyncSession, limit: int, offset: int,
                authors_ids: list[int] = None, available_copies_min: int = None, available_copies_max: int = None
    ):
        stmt = select(Book)

        # Фильтрация по авторам
        if authors_ids:
            stmt = stmt.join(Author, Book.authors).where(Author.id.in_(authors_ids))

        # Фильтрмация по количеству доступных экземпляров
        if available_copies_min is not None:
            stmt = stmt.where(Book.available_copies >= available_copies_min)
        if available_copies_max is not None:
            stmt = stmt.where(Book.available_copies <= available_copies_max)

        return await session.scalars(stmt.limit(limit).offset(offset))



