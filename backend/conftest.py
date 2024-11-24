import os
import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from httpx import AsyncClient

load_dotenv()
os.environ["ENV"] = "test"

from app.server import app  # noqa: E402
from core.db import Base  # noqa: E402
from core.config import config  # noqa: E402
from tests.seed_test_db import seed_db  # noqa: E402


@pytest.fixture()
def fastapi_client():
    return TestClient(app)


@pytest.fixture()
def client():
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture()
async def admin_token_headers(client: AsyncClient) -> dict[str, str]:
    login_data = {
        "username": "admin",
        "password": "admin",
    }
    response = await client.post("/api/latest/auth/login", json=login_data)

    assert response.status_code == 200, "Login failure"

    response = response.json()
    access_token = response["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture()
async def normal_user_token_headers(client: AsyncClient) -> dict[str, str]:
    login_data = {
        "username": "normal_user",
        "password": "normal_user",
    }
    response = await client.post("/api/latest/auth/login", json=login_data)

    assert response.status_code == 200, "Login failure"

    response = response.json()
    access_token = response["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture()
async def users(
    client: AsyncClient,
    admin_token_headers: dict[str, str],
) -> list[dict[str, str]]:
    res = await client.get("/api/v1/users", headers=await admin_token_headers)
    return res.json()


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    generate_database()


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    ...


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    ...


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """


def generate_database():
    if os.path.isfile("test.db"):
        os.remove("test.db")

    engine = create_engine(
        config.DB_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    engine.dispose()
    seed_db()
