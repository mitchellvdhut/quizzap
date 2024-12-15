"""
Documentation for the types of connection codes the server accepts
and returns.
"""

from core.helpers.websocket.docs import actions
from core.helpers.websocket.schemas.docs import (
    RequestWebSocketDocsSchema,
    ResponseWebSocketDocsSchema,
    WebSocketDocsSchema,
    WebSocketPacketParams,
)
from core.enums.websocket import QuizSessionActionEnum


quiz_actions = {a: actions[a] for a in actions}


quiz_actions[QuizSessionActionEnum.SESSION_CREATED] = WebSocketDocsSchema(
    info="Action after successfully creating an internal session.",
    response=ResponseWebSocketDocsSchema(
        info="session_id for inviting other users.",
        params=WebSocketPacketParams(payload={"session_id": "string"}),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_INFO] = WebSocketDocsSchema(
    info="Action for providing question data.",
    response=ResponseWebSocketDocsSchema(
        info="Response with question data.",
        params=WebSocketPacketParams(payload={"question": "<QuestionSchema>"}),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_START] = WebSocketDocsSchema(
    info="Action for indicating the start of the next question.",
    request=RequestWebSocketDocsSchema(
        info="Request the start of the next question as the session leader/admin.",
    ),
    response=ResponseWebSocketDocsSchema(
        info="Provides amount of answers to choose from.",
        params=WebSocketPacketParams(payload={"answer_count": "integer"}),
    ),
)

quiz_actions[QuizSessionActionEnum.SUBMIT_VOTE] = WebSocketDocsSchema(
    info="Action for submitting a vote on the current question.",
    request=RequestWebSocketDocsSchema(
        info="Request the submittion of a vote for the current question",
        params=WebSocketPacketParams(payload={"vote": "integer"}),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_STOP] = WebSocketDocsSchema(
    info="Action for indicating the end of a question.",
    request=RequestWebSocketDocsSchema(
        info="Request the end of the current question as the session leader/admin.",
    ),
    response=ResponseWebSocketDocsSchema(
        info="Indicates the end of the current question.",
    ),
)

quiz_actions[QuizSessionActionEnum.SCORE_INFO] = WebSocketDocsSchema(
    info="Action for providing player scores.",
    response=ResponseWebSocketDocsSchema(
        info="Provides score information of all players in session.",
        params=WebSocketPacketParams(
            payload={
                "users": [
                    {"username": "string", "score": "integer", "streak": "integer"}
                ]
            }
        ),
    ),
)

quiz_actions[QuizSessionActionEnum.QUIZ_END] = WebSocketDocsSchema(
    info="Action for indicating the end of a quiz.",
    response=ResponseWebSocketDocsSchema(
        info="Indicates end of quiz.",
    ),
)
