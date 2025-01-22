from httpx import AsyncClient
from fastapi import status
import logging
logger = logging.getLogger(__name__)


async def test_all_books_filter(auth_reader_ac: AsyncClient):
    response = await auth_reader_ac.get(f"/book/", params={
        "authors": [1, 2],
        "available_copies_min": 3
    })
    response_body = response.json()
    logger.info(response_body)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_body) == 1
    assert response_body[0]["title"] == "Гордость и предубеждение"