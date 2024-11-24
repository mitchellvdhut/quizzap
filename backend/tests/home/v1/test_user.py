import pytest
from httpx import AsyncClient
from fastapi import Response

from core.helpers.hashids import encode


@pytest.mark.asyncio
async def test_get_users_as_admin(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_users_as_user(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    normal_headers = await normal_user_token_headers

    res = await client.get("/api/v1/users", headers=normal_headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_users_as_none(client: AsyncClient):
    res = await client.get("/api/v1/users")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers
    
    user_id = encode(100000)
    res = await client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "user3", "password": "user3"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "user3"


@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "user3", "password": "user3"}
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_as_normal_on_self(client: AsyncClient, normal_user_token_headers: dict[str, str], users: list[dict]):
    user_headers = await normal_user_token_headers
    users = await users
    user_id = users[1]["id"]

    res = await client.patch(f"/api/v1/users/{user_id}", headers=user_headers, json={"username": "bla", "password": "bla"})
    assert res.status_code == 200

    assert res.json()["username"] == "bla"

    res = await client.patch(f"/api/v1/users/{user_id}", headers=user_headers, json={"username": "normal_user", "password": "normal_user"})
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_update_user_as_normal_on_other(client: AsyncClient, normal_user_token_headers: dict[str, str], users: list[dict]):
    user_headers = await normal_user_token_headers
    users = await users
    user_id = users[0]["id"]

    res = await client.patch(f"/api/v1/users/{user_id}", headers=user_headers, json={"username": "bla", "password": "bla"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_update_user_as_admin_on_other(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers
    
    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    user_id = users[1]["id"]

    res = await client.patch(f"/api/v1/users/{user_id}", headers=admin_headers, json={"username": "bla", "password": "bla"})
    assert res.status_code == 200

    assert res.json()["username"] == "bla"

    res = await client.patch(f"/api/v1/users/{user_id}", headers=admin_headers, json={"username": "normal_user", "password": "normal_user"})
    assert res.status_code == 200

    user_id = encode(100000)
    res = await client.patch(f"/api/v1/users/{user_id}", headers=admin_headers, json={"username": "normal_user_3", "password": "normal_user_3"})
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_as_normal_on_self(client: AsyncClient, users: list[dict]):
    login_data = {
        "username": "user3",
        "password": "user3"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200, "Login failure"

    response = response.json()
    access_token = response["access_token"]

    users = await users
    user_id = users[2]["id"]

    res = await client.delete(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204
    

@pytest.mark.asyncio
async def test_delete_user_as_normal_on_other(client: AsyncClient, normal_user_token_headers: dict[str, str], users: list[dict]):
    normal_headers = await normal_user_token_headers
    users = await users
    user_id = users[0]["id"]

    res = await client.delete(f"/api/v1/users/{user_id}", headers=normal_headers)
    assert res.status_code == 401
    

@pytest.mark.asyncio
async def test_delete_user_as_admin_on_other(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers

    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "user3", "password": "user3"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "user3"
    
    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    user_id = users[2]["id"]

    res = await client.delete(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert res.status_code == 204

    res = await client.delete(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_path_user_id(client: AsyncClient, admin_token_headers):
    admin_headers = await admin_token_headers
    
    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()
    user_id = users[1]["id"]

    res = await client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert res.status_code == 200

    res = await client.get("/api/v1/users/", headers=admin_headers)
    assert res.status_code == 307

    res = await client.get("/api/v1/users/_", headers=admin_headers)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_bad_hash_id(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers

    response = await client.get("/api/v1/users/abc", headers=admin_headers)

    assert response.status_code == 400
