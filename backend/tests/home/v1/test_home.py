import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_home(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
