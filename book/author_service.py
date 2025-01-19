from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models import Author
from schemas import SAuthorCreate, SAuthorUpdate
from fastapi import HTTPException, status
from utils import copy_model_attributes


class AuthorService:

    author_not_found = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

    @classmethod
    async def create_author(cls, session: AsyncSession, author_create: SAuthorCreate) -> Author:
        author_dict = author_create.model_dump(exclude_unset=True)
        new_author = Author(**author_dict)
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author

    @classmethod
    async def update_author(cls, session: AsyncSession, author_id: int, author_update: SAuthorUpdate) -> Author:
        author = await session.get(Author, author_id)
        if not author:
            raise cls.author_not_found
        author_dict = author_update.model_dump(exclude_unset=True)
        copy_model_attributes(data=author_dict, model_to=author)
        await session.commit()
        await session.refresh(author)
        return author

    @classmethod
    async def get_author_by_id(cls, session: AsyncSession, author_id: int) -> Author:
        author = await session.get(Author, author_id)
        if not author:
            raise cls.author_not_found
        return author

    @classmethod
    async def delete_author(cls, session: AsyncSession, author_id: int):
        author = await session.get(Author, author_id)
        await session.delete(author)
        await session.commit()

