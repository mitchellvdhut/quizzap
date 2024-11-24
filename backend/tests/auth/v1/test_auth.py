import pytest
from httpx import AsyncClient
from core.db.models import User
from core.exceptions.base import CustomException
from core.fastapi.dependencies.permission import BasePermission
from core.helpers.hashids import encode

from core.helpers.token import token_checker
from core.helpers.token.token_helper import TokenHelper


@pytest.mark.asyncio
async def test_login_bad_creds(client: AsyncClient):
    data = {
        "username": "bla",
        "password": "bla"
    }
    response = await client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 401

    data = {
        "username": "admin",
        "password": "bla"
    }
    response = await client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 401

    data = {
        "username": "bla",
        "password": "admin"
    }
    response = await client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_tokens(client: AsyncClient):
    data = {
        "username": "admin",
        "password": "admin"
    }
    response = await client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 200

    tokens = response.json()
    data = tokens

    response = await client.post("/api/v1/auth/refresh", json=data)

    assert response.status_code == 200

    response = await client.post("/api/v1/auth/refresh", json=tokens)
    
    assert response.status_code == 401


def test_coverage_token_checker():
    id_ = token_checker.generate_add()
    token_checker.__repr__()
    token_checker._remove_tree(id_)

    with pytest.raises(KeyError) as excinfo:
        token_checker.add("a", "b")

    assert "Previous Id does not exist" in str(excinfo.value)

    token_checker.add("a")
    
    with pytest.raises(ValueError) as excinfo:
        token_checker.add("a")

    assert "Id key already exists" in str(excinfo.value)
    token_checker.add("b", "a")
    token_checker._remove_tree("b")


@pytest.mark.asyncio
async def test_bad_token(client: AsyncClient):
    TokenHelper.encode_refresh()  # Test coverage
    headers = {
        "Authorization": "Lmao"
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401

    headers = {
        "Authorization": "Bearer Lmao"
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401

    headers = {
        "Authorization": "bad Lmao"
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401

    headers = {
        "Authorization": "Bearer "
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401

    token = TokenHelper.encode({"thing": "athing", "sub": "access"}, -3600) 
    headers = {
        "Authorization": f"Bearer {token}z"
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_expired_token(client: AsyncClient):
    token = TokenHelper.encode({"thing": "athing", "sub": "access"}, -3600) 
    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = await client.get("/api/v1/users", headers=headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_incorrect_hash_user_token(client: AsyncClient):
    token = TokenHelper.encode_access({"user_id": 0})
    headers = {
        "Authorization": f"Bearer {token}"
    }
    x = False
    try:
        await client.get("/api/v1/users", headers=headers)
    except CustomException:
        x = True
    assert x, "Did not raise"


@pytest.mark.asyncio
async def test_token_no_user(client: AsyncClient):
    token = TokenHelper.encode_access({"user_id": encode(10000)})
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/users", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_base_permission_coverage():
    await BasePermission.has_permission(0, 0, 0)


def test_base_exception_coverage():
    exc = CustomException("Message")
    str(exc)

def test_user_model_coverage():
    user = User(username="a", password="b")
    str(user)