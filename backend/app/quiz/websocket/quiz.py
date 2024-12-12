"""Module containing the base websocket service for other variations to extend upon.
"""

from datetime import datetime, timedelta
import random
from fastapi import WebSocket
from app.user.services.user import UserService
from app.quiz.schemas.websocket import PoolData, UserData, UserScore
from app.quiz.services.quiz import QuizService
from app.question.schemas.question import QuestionSchema
from core.helpers.websocket.websocket import WebSocketConnection
from core.db.models import Question
from core.helpers.logger import log_exc
from core.exceptions.token import DecodeTokenException
from core.db.session import get_session
from core.helpers.hashids import decode_single
from core.helpers.token.token_helper import TokenHelper
from core.exceptions.websocket import (
    AccessDeniedException,
    AlreadyVotedException,
    InvalidVoteException,
    NoQuestionException,
    QuizStoppedException,
    RequestSuccessful,
    SessionNotFoundException,
    SuccessfullConnection,
)
from core.helpers.websocket import manager
from core.enums.websocket import QuizSessionActionEnum, WebsocketActionEnum
from core.helpers.websocket.schemas.packet import QuizWebsocketPacketSchema
from core.helpers.websocket.base import BaseWebsocketService
from core.helpers.websocket.permission.permission_dependency import PermList


class QuizWebsocketService(BaseWebsocketService):
    def __init__(
        self,
        websocket: WebSocket,
        perms: PermList | None = None,
    ):
        actions = {
            WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
            WebsocketActionEnum.SESSION_CLOSE.value: self.handle_session_close,
            QuizSessionActionEnum.SUBMIT_VOTE: self.handle_sumbit_vote,
            QuizSessionActionEnum.QUESTION_START: self.handle_question_start_request,
            QuizSessionActionEnum.QUESTION_STOP: self.handle_question_stop_request,
        }

        super().__init__(
            manager,
            websocket,
            perms,
            QuizWebsocketPacketSchema,
            actions,
        )

    @log_exc
    async def start_create_session(
        self,
        quiz_id: int,
        access_token: str,
        client_token: str,
    ):
        await self.create_session()
        await self.manager.connect(self.ws, self.pool_id)

        if not await self.manager.check_auth(
            *self.perms,
            access_token=access_token,
        ):
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        @get_session
        async def get_user(session):
            try:
                info = TokenHelper.decode(token=access_token)
                user_id = decode_single(info["user_id"])

            except DecodeTokenException:
                user_id = 1

            return await UserService(session).get_user(user_id)

        @get_session
        async def get_quiz(session):
            return await QuizService(session).get_quiz_loaded(quiz_id)

        user = await get_user()
        quiz = await get_quiz()

        if not user:
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        pool_data: PoolData = {
            "quiz": quiz,
            "question_index": -1,
            "question": None,
            "question_stop": None,
            "is_stopping": None,
            "question_active": False,
        }
        user_data: UserData = {
            "username": user.username,
            "is_admin": True,
            "score": 0,
            "streak": 0,
            "is_player": False,
            "vote": None,
            "voted_at": None,
            "client_token": client_token
        }

        self.manager.set_data(self.pool_id, pool_data)
        self.manager.set_client_data(self.pool_id, self.ws.id, user_data)

        await self.ws.status_code(SuccessfullConnection)
        await self.handle_created_session(self.pool_id)

        await self.handler()

    @log_exc
    async def start_join_session(
        self,
        session_id: int,
        username: str,
        client_token: str,
    ):
        self.pool_id = session_id

        if not self.manager.active_pools.get(session_id):
            self.pool_id = "disconnect"
            await self.manager.connect(self.ws, self.pool_id)
            await self.handle_session_not_found()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        await self.manager.connect(self.ws, self.pool_id)

        if not await self.manager.check_auth(*self.perms):
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        user_data: UserData = {
            "username": username,
            "is_admin": False,
            "score": 0,
            "streak": 0,
            "is_player": True,
            "vote": None,
            "voted_at": None,
            "client_token": client_token
        }

        new_join = True

        for cl_id, client in self.manager.active_pools[self.pool_id]["clients"].items():
            data: UserData = client["data"]
            if data["client_token"] == client_token:
                user_data = data
                del self.manager.active_pools[self.pool_id]["clients"][cl_id]
                new_join = False
                break

        self.manager.set_client_data(self.pool_id, self.ws.id, user_data)

        await self.ws.status_code(SuccessfullConnection)

        if new_join:
            await self.handle_user_joined(username)

        await self.handler()

    async def process(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        await self.handle_question_process()

    async def handle_question_process(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        if not self.is_admin(self.ws.id):
            return

        data: PoolData = self.manager.get_data(self.pool_id)

        all_answered = all(
            not client["data"]["is_player"] or client["data"]["vote"] is not None
            for client in self.manager.active_pools[self.pool_id]["clients"].values()
        )

        if data["is_stopping"]:
            if datetime.now() >= data["is_stopping"]:
                data["is_stopping"] = None

                await self.handle_question_finish()

        elif data["question_stop"]:
            if all_answered or datetime.now() >= data["question_stop"]:
                data["question_stop"] = None
                data["is_stopping"] = datetime.now() + timedelta(seconds=0.5)

                await self.handle_question_end()

        self.manager.set_data(self.pool_id, data)

    async def handle_user_joined(
        self,
        username: str,
    ) -> None:
        packet = QuizWebsocketPacketSchema(
            status_code=100,
            action=WebsocketActionEnum.USER_CONNECT,
            message="user has connected",
            payload={"username": username},
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_session_not_found(self) -> None:
        await self.ws.status_code(SessionNotFoundException)

    async def create_session(self) -> None:
        while not self.pool_id or self.manager.active_pools.get(self.pool_id):
            self.pool_id = random.randint(100000, 999999)

    async def handle_created_session(
        self,
        session_id: int,
    ) -> None:
        packet = QuizWebsocketPacketSchema(
            status_code=201,
            action=QuizSessionActionEnum.SESSION_CREATED,
            message="created new session",
            payload={"session_id": session_id},
        )

        await self.ws.send(packet)

    async def handle_pool_message(
        self,
        packet: QuizWebsocketPacketSchema,
        message: str | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        user: UserData = self.manager.get_client_data(self.pool_id, self.ws.id)
        packet.payload["username"] = user["username"]

        await super().handle_pool_message(packet, message)

    async def handle_sumbit_vote(
        self,
        packet: QuizWebsocketPacketSchema,
        **kwargs,
    ) -> None:
        del kwargs

        pool_data: PoolData = self.manager.get_data(self.pool_id)
        user_data: UserData = self.manager.get_client_data(self.pool_id, self.ws.id)

        if not pool_data["question_active"]:
            await self.ws.status_code(NoQuestionException)
            return

        if user_data["vote"]:
            await self.ws.status_code(AlreadyVotedException)
            return

        if len(pool_data["question"].answers) <= packet.payload["vote"]:
            await self.ws.status_code(InvalidVoteException)
            return

        data: UserData = self.manager.get_client_data(self.pool_id, self.ws.id)

        data["vote"] = packet.payload["vote"]
        data["voted_at"] = datetime.now()

        self.manager.set_client_data(self.pool_id, self.ws.id, data)

        await self.ws.status_code(RequestSuccessful)

    async def handle_question_info(
        self,
        question: Question,
        **kwargs,
    ) -> None:
        del kwargs

        question_schema = QuestionSchema(**question.__dict__)

        packet = QuizWebsocketPacketSchema(
            status_code=200,
            action=QuizSessionActionEnum.QUESTION_INFO,
            message="retrieved question information",
            payload=question_schema.model_dump(),
        )

        await self.ws.send(packet)

    async def handle_question_start_request(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        if not await self.handle_is_pool_admin():
            return

        data: PoolData = self.manager.get_data(self.pool_id)

        if len(data["quiz"].questions) <= data["question_index"]:
            await self.ws.status_code(QuizStoppedException)
            return

        quiz = data["quiz"]
        question_index: int = data["question_index"] + 1

        question = quiz.questions[question_index]

        data["question"] = question
        data["question_active"] = True
        data["question_index"] = question_index
        data["question_start"] = datetime.now()
        data["question_stop"] = datetime.now() + timedelta(seconds=question.time_limit)

        self.manager.set_data(self.pool_id, data)

        for ws_id, client in self.manager.active_pools[self.pool_id]["clients"].items():
            if self.is_admin(ws_id):
                await self.handle_question_info(question=question)
            else:
                await self.handle_question_start_response(
                    question=question,
                    websocket=client["ws"],
                )

    async def handle_question_start_response(
        self,
        question: Question,
        websocket: WebSocketConnection | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        packet = QuizWebsocketPacketSchema(
            status_code=200,
            action=QuizSessionActionEnum.QUESTION_START,
            message="retrieved question information",
            payload={"answer_count": len(question.answers)},
        )

        if not websocket:
            websocket = self.ws

        await websocket.send(packet)

    async def handle_question_stop_request(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        if not await self.handle_is_pool_admin():
            return

        await self.handle_question_end()

    async def handle_question_stop_response(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        packet = QuizWebsocketPacketSchema(
            status_code=200,
            action=QuizSessionActionEnum.QUESTION_STOP,
            message="question stopped",
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_question_end(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        data: PoolData = self.manager.get_data(self.pool_id)

        self.manager.set_data(self.pool_id, data)

        await self.handle_question_stop_response()

    async def handle_question_finish(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        data: PoolData = self.manager.get_data(self.pool_id)
        answers = [i.is_correct for i in data["question"].answers]

        for client in self.manager.active_pools[self.pool_id]["clients"].values():
            user_data: UserData = client["data"]

            if not user_data["is_player"]:
                continue

            is_correct = answers[user_data["vote"]]
            points = 0

            if is_correct:
                user_data["streak"] += 1

                # https://support.kahoot.com/hc/en-us/articles/115002303908-How-points-work

                limit = data["question"].time_limit
                user_vote_after = user_data["voted_at"] - data["question_start"]

                mult = 1 - ((user_vote_after.total_seconds() / limit) / 2)

                points = int(1000 * mult) + 100 * (user_data["streak"] - 1)

            else:
                user_data["streak"] = 0

            user_data["score"] = points

            user_data["vote"] = None
            user_data["voted_at"] = None

            client["data"] = user_data

        data["question"] = None
        data["question_start"] = None
        data["question_active"] = False

        await self.handle_score_info()

        if len(data["quiz"].questions) <= data["question_index"] + 1:
            await self.handle_quiz_end()

    async def handle_score_info(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        users: list[UserScore] = []

        for _, client in self.manager.active_pools[self.pool_id]["clients"].items():
            data: UserData = client["data"]

            if not data["is_player"]:
                continue

            users.append(
                {
                    "username": data["username"],
                    "score": data["score"],
                    "streak": data["streak"],
                }
            )

        packet = QuizWebsocketPacketSchema(
            status_code=200,
            action=QuizSessionActionEnum.SCORE_INFO,
            message="session user info",
            payload={"users": users},
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_quiz_end(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        packet = QuizWebsocketPacketSchema(
            status_code=200,
            action=QuizSessionActionEnum.QUIZ_END,
            message="quiz has ended",
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_is_pool_admin(
        self,
        **kwargs,
    ) -> bool:
        del kwargs

        if not self.is_admin(self.ws.id):
            await self.ws.status_code(AccessDeniedException)
            return False

        return True

    def is_admin(
        self,
        websocket_id: int,
    ) -> bool:
        return (
            self.manager.get_client_data(self.pool_id, websocket_id).get("is_admin")
            is True
        )
