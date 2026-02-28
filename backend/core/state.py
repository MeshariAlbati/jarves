from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class JarvesState(TypedDict):
    messages: Annotated[list, add_messages]
    goals: list[str]
    priorities: list[str]
    tasks: list[str]
    errors: list[str]
    user_id: str
    memory_context: str
    run_type: str
    final_response: str
    user_message: str
    intent: str
