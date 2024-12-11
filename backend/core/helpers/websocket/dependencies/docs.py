from typing import Any


def parse_actions(actions: dict[str, Any]) -> dict[str, str]:
    new_actions = {}
    for key, value in actions.items():
        new_actions[key.value] = value.model_dump()

    return new_actions
