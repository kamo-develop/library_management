import pytest
from httpx import AsyncClient
from fastapi import status
import logging

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("title, description, publication_date, genres, available_copies, authors, status_code", [
    ("Мертвые души", None, "1839-11-16", "Русская классика", 2, [3], status.HTTP_200_OK),
    (123, None, "1839-11-16", "Русская классика", 2, [3], status.HTTP_422_UNPROCESSABLE_ENTITY),                # Невалидные данные
    ("Мертвые души", None, "1839-11-16", "Русская классика", 2, [], status.HTTP_422_UNPROCESSABLE_ENTITY),      # Невалидные данные
    ("Мертвые души", None, "1839-11-16", "Русская классика", 2, [10], status.HTTP_404_NOT_FOUND),               # Отсутсвующий в базе автор
])
async def test_create_book(title, description, publication_date, genres, available_copies, authors, status_code, auth_admin_ac: AsyncClient):
    response = await auth_admin_ac.post("/book/", json={
        "title": title,
        "description": description,
        "publication_date": publication_date,
        "genres": genres,
        "available_copies": available_copies,
        "authors": authors
    })

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_body = response.json()
        assert response_body["title"] == title


async def test_update_book(auth_admin_ac: AsyncClient):
    book_id = 1
    publication_date = "1795-11-28"
    available_copies = 5
    response = await auth_admin_ac.patch(f"/book/{book_id}", json={
        "publication_date": publication_date,
        "available_copies": available_copies,
    })
    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert response_body["publication_date"] == publication_date
    assert response_body["available_copies"] == available_copies


@pytest.mark.parametrize("book_id, title, status_code", [
    (10, None, status.HTTP_404_NOT_FOUND),
    (2, "Портрет Дориана Грея", status.HTTP_200_OK),
    ("abc", None, status.HTTP_422_UNPROCESSABLE_ENTITY)
])
async def test_get_book(book_id, title, status_code, auth_reader_ac: AsyncClient):
    response = await auth_reader_ac.get(f"/book/{book_id}")
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_body = response.json()
        assert response_body["title"] == title


@pytest.mark.parametrize("book_id, status_code", [
    (10, status.HTTP_404_NOT_FOUND),
    (1, status.HTTP_200_OK),
])
async def test_delete_book(book_id, status_code, auth_admin_ac: AsyncClient):
    response = await auth_admin_ac.delete(f"/book/{book_id}")
    assert response.status_code == status_code

