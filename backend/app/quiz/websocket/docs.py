"""
Documentation for the types of connection codes the server accepts
and returns.
"""

from core.helpers.websocket.docs import actions
from core.helpers.websocket.schemas.docs import (
    RequestWebsocketDocsSchema,
    ResponseWebsocketDocsSchema,
    WebsocketDocsSchema,
    WebsocketPacketParams,
)
from core.enums.websocket import QuizSessionActionEnum


quiz_actions = {a: actions[a] for a in actions}


quiz_actions[QuizSessionActionEnum.SESSION_CREATED] = WebsocketDocsSchema(
    info="Action after successfully creating an internal session.",
    response=ResponseWebsocketDocsSchema(
        info="session_id for inviting other users.",
        params=WebsocketPacketParams(payload={"session_id": "string"}),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_INFO] = WebsocketDocsSchema(
    info="Action for providing question data.",
    response=ResponseWebsocketDocsSchema(
        info="Response with question data.",
        params=WebsocketPacketParams(payload="<QuestionSchema>"),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_START] = WebsocketDocsSchema(
    info="Action for indicating the start of the next question.",
    request=RequestWebsocketDocsSchema(
        info="Request the start of the next question as the session leader/admin.",
    ),
    response=ResponseWebsocketDocsSchema(
        info="Provides amount of answers to choose from.",
        params=WebsocketPacketParams(payload={"answer_count": "integer"}),
    ),
)

quiz_actions[QuizSessionActionEnum.SUBMIT_VOTE] = WebsocketDocsSchema(
    info="Action for submitting a vote on the current question.",
    request=RequestWebsocketDocsSchema(
        info="Request the submittion of a vote for the current question",
        params=WebsocketPacketParams(payload={"vote": "integer"}),
    ),
)

quiz_actions[QuizSessionActionEnum.QUESTION_STOP] = WebsocketDocsSchema(
    info="Action for indicating the end of a question.",
    request=RequestWebsocketDocsSchema(
        info="Request the end of the current question as the session leader/admin.",
    ),
    response=ResponseWebsocketDocsSchema(
        info="Indicates the end of the current question.",
    ),
)

quiz_actions[QuizSessionActionEnum.SCORE_INFO] = WebsocketDocsSchema(
    info="Action for providing player scores.",
    response=ResponseWebsocketDocsSchema(
        info="Provides score information of all players in session.",
        params=WebsocketPacketParams(
            payload={
                "users": [
                    {"username": "string", "score": "integer", "streak": "integer"}
                ]
            }
        ),
    ),
)
