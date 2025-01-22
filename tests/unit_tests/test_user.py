from httpx import AsyncClient
from fastapi import status
import pytest

@pytest.mark.parametrize("username, password, status_code", [
    ("user01", "123", status.HTTP_200_OK),
    ("user01", "1235", status.HTTP_409_CONFLICT),
    ("user03", 1235, status.HTTP_422_UNPROCESSABLE_ENTITY),
])
async def test_register_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/user/register", json={
        "username": username,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("username, password, status_code", [
    ("Ivan", "1234", status.HTTP_401_UNAUTHORIZED),
    ("Alexandr", "qwerty", status.HTTP_401_UNAUTHORIZED),
    ("admin", "123", status.HTTP_200_OK),
])
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/user/login", data={
        "username": username,
        "password": password
    })
    assert response.status_code == status_code
