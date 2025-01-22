import pytest
from httpx import AsyncClient
from fastapi import status
import logging

logger = logging.getLogger(__name__)


async def test_create_author_no_permission(auth_reader_ac: AsyncClient):
    response = await auth_reader_ac.post("/author/", json={
        "name": "Лев Толстой",
        "birth_date": "1828-09-09"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("name, biography, birth_date, status_code", [
    ("Лев Толстой", None, "1828-09-09", status.HTTP_200_OK),
    (None, None, "1828-09-09", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("Фёдор Достоевский", None, "1821", status.HTTP_422_UNPROCESSABLE_ENTITY),
])
async def test_create_author(name, biography, birth_date, status_code, auth_admin_ac: AsyncClient):
    response = await auth_admin_ac.post("/author/", json={
        "name": name,
        "biography": biography,
        "birth_date": birth_date
    })
    assert response.status_code == status_code


async def test_update_author(auth_admin_ac: AsyncClient):
    author_id = 3
    new_name = "Николай Васильевич Гоголь"
    response = await auth_admin_ac.patch(f"/author/{author_id}", json={
        "name": new_name,
    })
    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert response_body["name"] == new_name


@pytest.mark.parametrize("author_id, name, status_code", [
    (10, None, status.HTTP_404_NOT_FOUND),
    (1, "Джейн Остин", status.HTTP_200_OK),
    ("abc", None, status.HTTP_422_UNPROCESSABLE_ENTITY)
])
async def test_get_author(author_id, name, status_code, auth_reader_ac: AsyncClient):
    response = await auth_reader_ac.get(f"/author/{author_id}")
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        response_body = response.json()
        assert response_body["name"] == name


@pytest.mark.parametrize("author_id, status_code", [
    (2, status.HTTP_409_CONFLICT),      # Попытка удалить автора, у которого в базе есть книга
    (3, status.HTTP_200_OK),
])
async def test_delete_author(author_id, status_code, auth_admin_ac: AsyncClient):
    response = await auth_admin_ac.delete(f"/author/{author_id}")
    assert response.status_code == status_code