import pytest
from httpx import AsyncClient
from fastapi import Response


@pytest.mark.asyncio
async def test_get_me_no_auth(client: AsyncClient):
    response = await client.get("/api/v1/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    user_headers = await normal_user_token_headers

    response_me = await client.get("/api/v1/me", headers=user_headers)
    assert response_me.status_code == 200, "Login failure"


@pytest.mark.asyncio
async def test_update_me_no_auth(client: AsyncClient):
    response = await client.patch("/api/v1/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_me(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    user_headers = await normal_user_token_headers

    response = await client.patch("/api/v1/me", headers=user_headers, json={"username": "Turtle", "password": "stew"})
    data = response.json()
    assert data.get("username")
    assert response.status_code == 200

    response = await client.patch("/api/v1/me", headers=user_headers, json={"username": "normal_user", "password": "normal_user"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_me_no_auth(client: AsyncClient):
    response = await client.delete("/api/v1/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_me(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "temp_user", "password": "temp_user"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "temp_user"

    login_data = {
        "username": "temp_user",
        "password": "temp_user"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200, "Login failure"

    response = response.json()
    access_token = response["access_token"]

    res = await client.delete("/api/v1/me", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204, "Delete failure"
