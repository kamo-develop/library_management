from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError
from exceptions import AuthorNotFoundException, AuthorHasBookException
from models import Author
from schemas import SAuthorCreate, SAuthorUpdate
from utils import copy_model_attributes
import logging

logger = logging.getLogger(__name__)

class AuthorService:

    @classmethod
    async def create_author(cls, session: AsyncSession, author_create: SAuthorCreate) -> Author:
        author_dict = author_create.model_dump(exclude_unset=True)
        new_author = Author(**author_dict)
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        logger.info(f"Created new author: {new_author}")
        return new_author

    @classmethod
    async def update_author(cls, session: AsyncSession, author_id: int, author_update: SAuthorUpdate) -> Author:
        author = await cls.get_author_by_id(session, author_id)
        author_dict = author_update.model_dump(exclude_unset=True)
        copy_model_attributes(data=author_dict, model_to=author)
        await session.commit()
        await session.refresh(author)
        logger.info(f"Updated author: {author}")
        return author

    @classmethod
    async def get_author_by_id(cls, session: AsyncSession, author_id: int) -> Author:
        author = await session.get(Author, author_id)
        if not author:
            raise AuthorNotFoundException
        return author

    @classmethod
    async def delete_author(cls, session: AsyncSession, author_id: int):
        try:
            author = await cls.get_author_by_id(session, author_id)
            await session.delete(author)
            await session.commit()
            logger.info(f"Deleted author with id={author_id}")
        except IntegrityError as e:
            logger.warning(e)
            raise AuthorHasBookException

    @classmethod
    async def get_all_authors(cls, session: AsyncSession, limit: int, offset: int):
        return await session.scalars(select(Author).limit(limit).offset(offset))

