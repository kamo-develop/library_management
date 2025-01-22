import pytest
from httpx import AsyncClient
from fastapi import status
import logging

logger = logging.getLogger(__name__)



async def test_borrowing_books_max_limit(auth_reader_ac: AsyncClient):
    book_ids = [1, 2, 3, 1, 2]
    for book_id in book_ids:
        response = await auth_reader_ac.post(f"/borrowing/{book_id}")
        assert response.status_code == status.HTTP_200_OK

    response = await auth_reader_ac.post(f"/borrowing/{1}")
    assert response.status_code == status.HTTP_409_CONFLICT