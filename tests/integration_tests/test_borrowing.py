import pytest
from httpx import AsyncClient
from fastapi import status
import logging

logger = logging.getLogger(__name__)



async def test_borrowing_books_max_limit(auth_reader_ac: AsyncClient):
    book_ids = [1, 2, 3, 1, 2]
    # Выдача книг
    for book_id in book_ids:
        response = await auth_reader_ac.post(f"/borrowing/{book_id}")
        assert response.status_code == status.HTTP_200_OK

    # Попытка взять 6ю книгу
    response = await auth_reader_ac.post(f"/borrowing/{1}")
    assert response.status_code == status.HTTP_409_CONFLICT

    # Возврат книг
    for book_id in book_ids:
        response = await auth_reader_ac.post(f"/borrowing/return/{book_id}")
        assert response.status_code == status.HTTP_200_OK


async def test_borrowing_books_available_copies(auth_reader_ac: AsyncClient):
    book_id = 4
    # Выдача книги
    response = await auth_reader_ac.post(f"/borrowing/{book_id}")
    response_body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_body["book"]["available_copies"] == 0

    # Получение записей о всех книгах на руках читателя (должна быть 1)
    response = await auth_reader_ac.get("/borrowing/all")
    borrowing_list = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(borrowing_list) == 1

    # Вовзврат книги
    response = await auth_reader_ac.post(f"/borrowing/return/{book_id}")
    response_body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_body["book"]["available_copies"] == 1

    # Получение записей о всех книгах на руках читателя  (должно быть 0)
    response = await auth_reader_ac.get("/borrowing/all")
    borrowing_list = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(borrowing_list) == 0
