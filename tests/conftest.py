import asyncio
import json
from datetime import datetime
import pytest
from httpx import AsyncClient, ASGITransport
from config import settings
from database import Base, engine, async_session
from models import User, Author, Book, Borrowing, book_author_association
from sqlalchemy import insert, text
from main import app as fastapi_app
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    """ Подготовка базы данных для тестирования """

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    # Считывание тестовых данных из файлов
    users = open_mock_json("users")
    authors = open_mock_json("authors")
    books = open_mock_json("books")
    book_authors = []

    # Преобразование данных
    for author in authors:
        author["birth_date"] = datetime.strptime(author["birth_date"], "%Y-%m-%d")
    for book in books:
        book["publication_date"] = datetime.strptime(book["publication_date"], "%Y-%m-%d")

        # Пары ключей для связующей таблицы автор-книга
        for author in book["authors"]:
            book_authors.append({"author_id": author, "book_id": book["id"]})
        del book["authors"]

    async with async_session() as session:
        await session.execute(insert(User).values(users))
        await session.execute(insert(Author).values(authors))
        await session.execute(insert(Book).values(books))
        await session.execute(insert(book_author_association).values(book_authors))

        # Увеличение значения последовательностей, чтобы не было конфликтов id при добавлении новых сущностей во время тестирования
        await session.execute(text(f"ALTER SEQUENCE user_account_id_seq RESTART WITH {len(users) + 1}"))
        await session.execute(text(f"ALTER SEQUENCE author_id_seq RESTART WITH {len(authors) + 1}"))
        await session.execute(text(f"ALTER SEQUENCE book_id_seq RESTART WITH {len(books) + 1}"))

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_admin_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        response = await ac.post("/user/login", data={
            "username": "admin",
            "password": "123"
        })
        response_body = response.json()
        ac.headers.update({"Authorization": f"Bearer {response_body["access_token"]}"})
        yield ac


@pytest.fixture(scope="session")
async def auth_reader_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        response = await ac.post("/user/login", data={
            "username": "Ivan",
            "password": "12345"
        })
        response_body = response.json()
        ac.headers.update({"Authorization": f"Bearer {response_body["access_token"]}"})
        yield ac
