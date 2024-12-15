# pylint: skip-file
import asyncio
import pytest

from typing import Dict
from httpx import AsyncClient
from fastapi.testclient import TestClient
import pytest_asyncio
from starlette.testclient import WebSocketTestSession

import core.exceptions.websocket as exc
from core.enums.websocket import (
    WebSocketActionEnum as wae,
    QuizSessionActionEnum as qsae,
)


def receive(ws: WebSocketTestSession, timeout: float = 5):
    data = asyncio.run(asyncio.wait_for(
        ws.receive_json(),
        timeout=timeout,
    ))

    return data


def assert_status_code(data, exception):
    assert data.get("action") == wae.STATUS_CODE

    payload = data.get("payload")
    assert payload is not None

    assert payload.get("status_code") == exception.code
    assert payload.get("message") == exception.message


def strip_headers(header: str):
    return header.get("Authorization").split(" ")[1]


def send_vote(ws: WebSocketTestSession, vote: int):
    packet = {
        "action": qsae.SUBMIT_VOTE,
        "payload": {"vote": vote},
    }
    ws.send_json(packet)


def send_message(ws: WebSocketTestSession, message: str):
    packet = {"action": wae.POOL_MESSAGE, "payload": {"message": message}}
    ws.send_json(packet)


def send_start_question(ws: WebSocketTestSession):
    packet = {"action": qsae.QUESTION_START}
    ws.send_json(packet)


def send_stop_question(ws: WebSocketTestSession):
    packet = {"action": qsae.QUESTION_STOP}
    ws.send_json(packet)


def send_session_close(ws: WebSocketTestSession):
    packet = {"action": wae.SESSION_CLOSE}
    ws.send_json(packet)


def assert_packet(
    expected_action: wae | qsae,
    packet: dict[str, str],
) -> dict[str, str]:
    print(packet)
    assert packet["action"] == expected_action
    return packet["payload"]


@pytest_asyncio.fixture()
async def quizzes(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> list[Dict[str, str]]:
    res = await client.get("/api/v1/quizzes", headers=admin_token_headers)
    return res.json()


@pytest.mark.asyncio
async def test_action_docs(client: AsyncClient):
    res = await client.get("/api/v1/sockets/quiz/action_docs")
    docs = res.json()

    assert res.status_code == 200
    assert type(docs) is dict

    assert len(docs) == len([a.value for a in qsae]) + len([a.value for a in wae])
    for action in qsae:
        assert action.value in [a for a in docs]
    for action in wae:
        assert action.value in [a for a in docs]


class MultiConnection:
    def __init__(self, client: TestClient, create_url: str, *join_urls: str):
        self.create_url = create_url
        self.join_urls = join_urls
        self.client = client
        self.contexts = []

    def __enter__(self):
        ws_admin: WebSocketTestSession = self.client.websocket_connect(self.create_url)
        test = self.client.websocket_connect("")
        print(test)
        print(ws_admin)
        raise Exception("Cry")

        print("receive 1")
        data_admin = receive(ws_admin)

        assert_status_code(data_admin, exc.SuccessfullConnection)

        print("receive 2")
        data_admin = assert_packet(qsae.SESSION_CREATED, receive(ws_admin))

        session_id = data_admin["session_id"]

        join_urls = [i.replace("<session_id>", session_id) for i in self.join_urls]

        self.contexts = [ws_admin]

        for url in join_urls:
            ws_user = self.client.websocket_connect(url)
            self.contexts.append(ws_user)

        return self.contexts

    def __exit__(self):
        [ws.close() for ws in self.contexts]


@pytest.mark.asyncio
async def test_quiz_session_1(
    fastapi_client: TestClient,
    admin_token_headers: Dict[str, str],
    normal_user_token_headers: Dict[str, str],
):
    quiz_id = ""
    access_token = strip_headers(admin_token_headers)
    admin_client_token = "abc"
    user_client_token = "def"
    username = "some user"

    create_url = f"/api/latest/sockets/quizCreate/{quiz_id}?access_token={access_token}&client_token={admin_client_token}"
    join_url = f"/api/latest/sockets/quizJoin/<session_id>?username={username}&client_token={user_client_token}"

    # NOTE to self: receive() functions wait until they receive any data
    # and if they do not receive anything, they wait 'til the end of time
    with MultiConnection(fastapi_client, create_url, join_url) as ws_admin:
        print(ws_admin)
        ws_admin: WebSocketTestSession
        # ws_normal_user: WebSocketTestSession
