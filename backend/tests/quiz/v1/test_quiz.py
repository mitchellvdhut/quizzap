import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_quizzes(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    res = await client.get("/api/v1/quizzes", headers=normal_user_token_headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_quiz(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    res = await client.post(
        "/api/v1/quizzes",
        headers=normal_user_token_headers,
        json={"name": "new quiz", "description": "the new test quiz"},
    )
    assert res.status_code == 201

    data = res.json()
    assert data["name"] == "new quiz"


@pytest.mark.asyncio
async def test_update_quiz(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    res = await client.get("/api/v1/quizzes", headers=normal_user_token_headers)
    assert res.status_code == 200
    data = res.json()

    assert data[1]["name"] == "new quiz"

    res = await client.patch(
        f"/api/v1/quizzes/{data[1]['id']}",
        headers=normal_user_token_headers,
        json={"name": "new quiz but changed", "description": "the new test quiz"},
    )
    assert res.status_code == 200

    data = res.json()
    assert data["name"] == "new quiz but changed"


@pytest.mark.asyncio
async def test_delete_quiz(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
):
    res = await client.get("/api/v1/quizzes", headers=normal_user_token_headers)
    assert res.status_code == 200
    data = res.json()

    assert data[1]["name"] == "new quiz but changed"

    res = await client.delete(
        f"/api/v1/quizzes/{data[1]['id']}",
        headers=normal_user_token_headers,
    )
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_upload_quiz(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
):
    res = await client.get("/api/v1/quizzes", headers=normal_user_token_headers)
    assert res.status_code == 200
    data = res.json()

    assert data[0]["name"] == "The Greg quiz!"

    new_quiz = data[0]

    new_quiz['name'] = "very new quiz!"

    res = await client.put(
        "/api/v1/quizzes",
        headers=normal_user_token_headers,
        json=new_quiz
    )

    assert res.status_code == 200
    data = res.json()

    assert data['name'] == "very new quiz!"
    assert len(data['questions']) > 0
    assert len(data['questions'][0]['answers']) > 0
